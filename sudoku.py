import dlx

class Sudoku(object):
    def solve(self, grid_str):
        solver = dlx.DLX()
        solver.create_matrix(grid_str)
        dlx_solution, found = solver.search([])
        return dlx_solution, found

    def output_solution(self, dlx_solution, found):
        """Converts a solution set from Dancing Links into a grid"""
        if not found:
            print('Solution not found')
            return
        solution = [0] * 81
        for i in dlx_solution:
            val = i.row % 9
            if val == 0:
                val = 9
            solution[(i.row - 1) // 9] = val
        self.output_grid(''.join(str(i) for i in solution))

    def output_grid(self, grid_str):
        """Outputs Sudoku grid in a readable format"""
        print('')
        grid = list(grid_str)
        row = list('+-------+-------+-------+')
        for index, chr in enumerate(grid):
            if index % 9 == 0:
                print(''.join(row))
                if index % 27 == 0 and index > 0:
                    print('+-------+-------+-------+')
                row = []
            if index % 3 == 0:
                row.extend(['|', ' '])
            row.extend([chr, ' '])
            if (index + 1) % 9 == 0:
                row.append('|')
            if index == len(grid_str) - 1:
                print(''.join(row))
                print('+-------+-------+-------+\n')

if __name__ == "__main__":
    s = Sudoku()
    print('Enter a sudoku puzzle in the format shown below:')
    print('7......5..5.98472383..2...9.79.58.4...........6.14.97.5...3..94126495.8..4......1\n')
    while 1:
        grid_str = input('')
        solution, found = s.solve(grid_str)
        s.output_solution(solution, found)
