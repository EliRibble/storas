"""Module for dealing with manifest files."""
import collections
import logging
import os
import typing
import urllib.parse
import xml.etree.ElementTree

DEFAULT_MANIFEST_FILE = "default.xml"
KNOWN_ELEMENTS = ("default", "include", "project", "remote")
LOGGER = logging.getLogger(__name__)

class ManifestParseError(Exception):
	"""Indicates a bad manifest file was found."""

class Remote():
	def __init__(self, name: typing.Text, fetch: typing.Text, review: typing.Text):
		self.fetch = urllib.parse.urlparse(fetch)
		self.fetch_host = self.fetch.netloc.split(".")[0]
		self.name = name
		self.review = urllib.parse.urlparse(review)

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "Remote {name} review {review} fetch {fetch}".format(
			fetch = self.fetch,
			name = self.name,
			review = self.review,
		)

class Manifest():
	"""Represents a bundle of manifest files."""

	def __init__(self, path: typing.Text):
		self.defaults = {}
		self.includes = []
		self.path = path
		self._projects = {}
		self.remotes = {}

	def get_remote(self, remote_name) -> Remote:
		for remote in self.remotes:
			if remote.name == remote_name:
				return remote
		raise IndexError("No such remote '{}'".format(remote_name))

	@staticmethod
	def parse(path: typing.Text, tree: xml.etree.ElementTree.ElementTree) -> "Manifest":
		root = tree.getroot()
		if not root.tag == "manifest":
			raise BadManifestError("Root node is not 'manifest'")
		result = Manifest(path)
		for child in root.getchildren():
			if child.tag == "default":
				result._handle_default(child)
			elif child.tag == "include":
				result._handle_include(child)
			elif child.tag == "project":
				result._handle_project(child)
			elif child.tag == "remote":
				result._handle_remote(child)
			else:
				raise NotImplementedError("No handler for {}".format(child.tag))
		result._add_parents()
		return result

	@property
	def projects(self):
		for manifest in self.includes:
			for project in manifest.projects:
				yield project
		for project in self._projects.values():
			yield project

	def _add_parents(self) -> None:
		project_by_path = {p.path: p for p in self.projects}
		for project in self.projects:
			parent_dir = project.path
			while parent_dir:
				#if parent_dir == "chromium/src":
					#import pdb;pdb.set_trace()
				parent_dir, _ = os.path.split(parent_dir)
				if parent_dir in project_by_path:
					project.parent = project_by_path[parent_dir]
					break

	def _handle_default(self, node: xml.etree.ElementTree.Element) -> None:
		for attribute in node.attrib.keys():
			assert attribute not in self.defaults
			self.defaults.update(node.attrib)
		LOGGER.debug("Updated defaults with %s", node.attrib)

	def _handle_include(self, node: xml.etree.ElementTree.Element) -> None:
		base = os.path.dirname(self.path)
		newpath = os.path.join(base, node.attrib["name"])
		submanifest = load(newpath)
		self.includes.append(submanifest)

	def _handle_project(self, node: xml.etree.ElementTree.Element) -> None:
		path = node.attrib.get("path")
		project = Project(
			self,
			name = node.attrib.get("name"),
			parent = None,
			path = path,
			remote = node.attrib.get("remote"),
			revision = node.attrib.get("revision"),
			sheriff = node.attrib.get("sheriff"),
		)
		self._projects[project.name] = project
		LOGGER.debug("Added project %s", project.name)

	def _handle_remote(self, node: xml.etree.ElementTree.Element) -> None:
		remote = Remote(
			fetch = node.attrib.get("fetch"),
			name = node.attrib.get("name"),
			review = node.attrib.get("review"),
		)
		self.remotes[remote.name] = remote
		LOGGER.debug("Added remote %s", remote.name)
		
class Project():
	"A single project in a manifest."
	def __init__(self,
			manifest: Manifest,
			name: typing.Text,
			remote: typing.Text,
			path: typing.Text=None,
			revision: typing.Text=None,
			parent: "Project"=None,
			sheriff: typing.Text=None,
		):
		self.manifest = manifest
		self.name = name
		self.parent = parent
		self.path = path or name
		self._remote = remote
		self.revision = revision or manifest.defaults.get("revision", "master")
		self.sheriff = sheriff

	@property
	def remote(self):
		return self.manifest.remotes[self._remote]

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "Project {name} at {path} from {remote} on {revision}".format(
			name = self.name,
			path = self.path,
			remote = self._remote,
			revision = self.revision,
		)

def load(manifest_path: typing.Text) -> Manifest:
	with open(manifest_path, "r") as r:
		tree = xml.etree.ElementTree.parse(r)
	LOGGER.debug("Loaded manifest XML file '%s'", manifest_path)
	return Manifest.parse(manifest_path, tree)

