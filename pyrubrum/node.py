# Pyrubrum - An intuitive framework for creating Telegram bots
# Copyright (C) 2020 Hearot <https://github.com/hearot>
#
# This file is part of Pyrubrum.
#
# Pyrubrum is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrubrum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrubrum. If not, see <http://www.gnu.org/licenses/>.

from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Tuple

from .base_menu import BaseMenu

Family = Tuple[Optional[BaseMenu], Optional[List[BaseMenu]]]


@dataclass(eq=False, init=False, repr=True)
class Node:
    """Representation of a single object in a tree, which might have defined a
    parent (i.e. the `Node` object it is child of) and a list of other nodes,
    which are its children. Each `Node` instance is linked to a subclass of
    `BaseMenu`.

    Attributes:
        menu (BaseMenu): The menu the node is linked to.
        children (Optional[List[Node]]): The nodes whose parent is this
            instance. Defaults to an empty list on initialization.
    """

    menu: BaseMenu
    children: Optional[List["Node"]]

    def __init__(
        self, menu: BaseMenu, children: Optional[List["Node"]] = None
    ):
        """Initialize a node by defining its children and linking it to a menu.

        Args:
            menu (BaseMenu): The menu this node is being linked to.
            children (Optional[List[Node]]): The nodes whose parent is going
                to be this instance. Defaults to ``None``, which makes the
                children list an empty one.
        """
        self.children = children if children else []
        self.menu = menu

    def add_child(self, node: "Node"):
        """Add a `Node` instance to the list of children.

        Args:
            node (Node): The node which is being added as a child of this
                object.
        """
        self.children.append(node)

    def get_children_menus(self) -> List[BaseMenu]:
        """Get all the menus that are linked to the children belonging to
        this instance.

        Returns:
            List[BaseMenu]: The list of the retrieved menus.
        """
        children = [child.menu for child in self.children]
        return children if children else None

    def get_family(self, menu_id: str, parent: Optional["Node"]) -> Family:
        """Retrieve the menus which are linked to both parent and children of this
        instance if this instance matches the provided identifier. Otherwise it
        will search the menu matching it in his children and return its family,
        if matched. On failure, it will return a tuple of length two filled
        with null values (i.e. ``None``).

        Args:
            menu_id (str): The identifier which must be matched.
            parent (Optional[Node]): The parent this ``Node`` comes from.

        Returns:
            Tuple[Optional[BaseMenu], Optional[List[BaseMenu]]]: A tuple of
                length two, whose first element is the parent node of the
                matched node while the second one is a list of all its children
                If no `Node` is found, the tuple will be filled with null
                values (i.e. ``None``).
        """
        if self.menu.menu_id == menu_id:
            return (
                parent.menu if isinstance(parent, Node) else None,
                self.get_children_menus(),
            )

        for child in self.children:
            child_menus = child.get_family(menu_id, self)

            if child_menus[0]:
                return child_menus

        return (None, None)

    def get_menus(self) -> List[BaseMenu]:
        """Retrieve the list of all the menus which are linked to the nodes belonging
        to the descent of this class (i.e. the children, the children of the
        children, etc...).

        Returns:
            List[BaseMenu]: The list of all the retrieved menus.
        """
        menus = [self.menu]

        for child in self.children:
            if child.menu.menu_id != self.menu.menu_id:
                menus += child.get_menus()

        return menus
