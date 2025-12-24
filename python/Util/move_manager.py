from Cube.constants import L, R, F2, B2, Li, Ri


# Cube faces that are opposite to each other
opposites = {'U':'D', 'D':'U', 'L':'R', 'R':'L', 'F':'B', 'B':'F'}


class MoveManager:
    
    def reduce_moves(moves: list[str]) -> list[str]:
        stack = []
        for move in moves:
            stack.append([move[0], int(move[1])])

            i = len(stack) - 2
            while i >= 0:
                if stack[i][0] == stack[-1][0]:
                    stack[i][1] += stack.pop()[1]
                    stack[i][1] %= 4
                    if stack[i][1] == 0: del stack[i]
                    i = len(stack) - 2 # restart
                elif stack[i][0] == opposites[stack[-1][0]]:
                    i -= 1
                else: break
    
        return [f'{face}{turns}' for face, turns in stack]

    
    def replace_u_moves(moves: list[str]) -> list[str]:
        replaced = []
        seq = [L, R, F2, B2, Li, Ri]
        for move in moves:
            if move[0] != 'U': replaced.append(move)
            else: replaced.extend(seq + ['D' + move[1]] + seq)
        return replaced
    

    def convert_to_pairs(moves: list[str]) -> list[tuple[str]]:
        pairs = []
        while moves:
            move1, move2 = moves.pop(), None
            if moves and moves[-1][0] == opposites[move1[0]]:
                move2 = moves.pop()
            pairs.append((move1, move2))
        return pairs
