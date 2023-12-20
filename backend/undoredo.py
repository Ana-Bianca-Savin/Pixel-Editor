from backend.canvas import Canvas
from backend.utilties import export

class UndoRedoManager:
    def __init__(self) -> None:
        self.undo_stack = []
        self.redo_stack = []

    def push_canvas(self, canvas : Canvas):
        # print('pushed canvas')

        canvas.update_top_texture()
        self.undo_stack.append(canvas.copy())
        self.redo_stack.clear()

    def undo(self) -> Canvas:
        if len(self.undo_stack) > 1:
            c = self.undo_stack.pop()
            self.redo_stack.append(c)
            return self.undo_stack[-1].copy()
        return None
    
    def redo(self) -> Canvas:
        if len(self.redo_stack) > 0:
            c = self.redo_stack.pop()
            self.undo_stack.append(c)
            return c.copy()
        return None