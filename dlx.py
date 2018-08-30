from math import inf

class Node(object):
    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.up, self.down, self.left, self.right = self, self, self, self

class ColumnNode(Node):
    def __init__(self, id):
        Node.__init__(self, self, id)
        self.row_count = 0

class DLX(object):
    def __init__(self):
        self.root = ColumnNode(0)

    def create_matrix(self, grid_str):
        """Creates an exact cover matrix from a sudoku grid"""
        root = self.root
        cols = [root]
        # Construct column headers as a doubly circular linked list
        # We'll be storing all the column headers in a list for easy access
        for i in range(324):
            c = ColumnNode(i + 1)
            c.right = root
            c.left = root.left
            root.left.right = c
            root.left = c
            cols.append(c)

        # These help us find which constraint should be filled in
        row_constraint = lambda x, k: 81 + (x // 9) * 9 + k
        col_constraint = lambda x, k: 162 + (x % 9) * 9 + k
        box_constraint = lambda x, k: 243 + (x // 27) * 27 + (x % 9) // 3 * 9 + k
        row_num = lambda x, k: x * 9 + k

        def _append_to_column(n):
            """Appends a row node at the end of a column"""
            c = n.column
            c.row_count += 1
            n.down = c
            n.up = c.up
            c.up.down = n
            c.up = n

        def _create_links(x, k):
            """Creates links for a row"""
            cell_node = Node(cols[x + 1], row_num(x, k))
            row_node = Node(cols[row_constraint(x, k)], row_num(x, k))
            col_node = Node(cols[col_constraint(x, k)], row_num(x, k))
            box_node = Node(cols[box_constraint(x, k)], row_num(x, k))

            # Link all the nodes into a single row
            cell_node.right, cell_node.left = row_node, box_node
            row_node.right, row_node.left = col_node, cell_node
            col_node.right, col_node.left = box_node, row_node
            box_node.right, box_node.left = cell_node, col_node

            _append_to_column(cell_node)
            _append_to_column(row_node)
            _append_to_column(col_node)
            _append_to_column(box_node)


        for index, chr in enumerate(grid_str):
            if chr == '.':
                # Square is empty, add all possible values
                for k in range(9):
                    _create_links(index, k + 1)
            else:
                _create_links(index, ord(chr) - 48)

    def choose_least_column(self):
        """
        We use the S heuristic to minimize branching factor
        Returns the column with the least number of rows
        """
        c = None
        i = self.root.right
        s = inf
        while i != self.root:
            if i.row_count < s:
                c = i
                s = i.row_count
            i = i.right
        return c

    def cover(self, col):
        """Removes a column along with all rows that intersect said column"""
        col.right.left = col.left
        col.left.right = col.right
        i = col.down
        while i != col:
            # Iterate through nodes in row and unlink them
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.column.row_count -= 1
                j = j.right
            i = i.down

    def uncover(self, col):
        """Undo covering of a column"""
        i = col.up
        while i != col:
            j = i.left
            while j != i:
                j.down.up = j
                j.up.down = j
                j.column.row_count += 1
                j = j.left
            i = i.up
        col.right.left = col
        col.left.right = col

    def search(self, solution):
        """Search for a solution from a exact cover matrix"""

        # No columns left, a solution is found
        if self.root == self.root.right:
            return solution, True

        c = self.choose_least_column()
        self.cover(c)

        i = c.down
        while i != c:
            solution.append(i)
            j = i.right
            while j != i:
                self.cover(j.column)
                j = j.right

            solution, found = self.search(solution)
            if found:
                return solution, True

            i = solution.pop()
            c = i.column
            j = i.left
            while j != i:
                self.uncover(j.column)
                j = j.left

            i = i.down

        self.uncover(c)
        return solution, False
