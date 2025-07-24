from manim import *

class HelloWorldOT(Scene):
    def construct(self):
        # 1. Define all mobjects and their final layout first
        document_text = Text("hello world")
        code_font_size = 24

        # Using MarkupText for syntax highlighting
        purple = "#C586C0"
        yellow = "#FFD700"
        string_color = "#CE9178"
        number_color = "#569CD6"

        code_lines = VGroup(
            MarkupText(
                f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"hello"</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=code_font_size,
            ),
            MarkupText(
                f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">1</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=code_font_size,
            ),
            MarkupText(
                f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"world"</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=code_font_size,
            ),
        ).arrange(DOWN, aligned_edge=LEFT)

        # Arrange and center the final group to determine final positions
        final_group = VGroup(document_text, code_lines).arrange(RIGHT, buff=1)
        final_group.move_to(ORIGIN)

        # 2. Start the animation sequence
        # Animate "hello world" appearing in the center
        # We create a new Text object for the animation to avoid conflicts
        anim_doc_text = Text("hello world").move_to(ORIGIN)
        self.play(Write(anim_doc_text))
        self.wait(2)

        # Animate it moving to its final position
        self.play(anim_doc_text.animate.move_to(document_text.get_center()))
        self.wait(1)
        
        # We'll position the highlight relative to the last letter of "hello" for accuracy.
        hello_part = anim_doc_text[0:5] # "hello"
        last_char_of_hello = anim_doc_text[4] # The 'o'
        # For "hello world", 'w' is at index 6. The slice should be up to 11.
        world_part = anim_doc_text[5:11]

        # Animate "hello" with highlight
        hello_highlight = SurroundingRectangle(hello_part, color=YELLOW, stroke_width=2, buff=0.05)
        self.play(Create(hello_highlight))
        self.wait(0.5)
        self.play(TransformFromCopy(hello_highlight, code_lines[0]), FadeOut(hello_highlight))
        self.wait(0.5)
        
        # Highlight the space by creating a rectangle positioned next to the 'o'
        char_width = last_char_of_hello.get_width() * 0.75
        char_height = anim_doc_text.get_height()
        space_highlight = Rectangle(
            width=char_width,
            height=char_height,
            color=YELLOW,
            stroke_width=2  # Make the outline thinner
        ).next_to(last_char_of_hello, RIGHT, buff=0)

        self.play(Create(space_highlight))
        self.wait(0.5)
        self.play(TransformFromCopy(space_highlight, code_lines[1]), FadeOut(space_highlight))
        self.wait(0.5)

        # Animate "world" with highlight
        world_highlight = SurroundingRectangle(world_part, color=YELLOW, stroke_width=2, buff=0.05)
        self.play(Create(world_highlight))
        self.wait(0.5)
        self.play(TransformFromCopy(world_highlight, code_lines[2]), FadeOut(world_highlight))
        self.wait(1)

        # "and lets call this sequence Operation A"
        # 1. Fade out "hello world" and center the operations simultaneously
        self.play(FadeOut(anim_doc_text), code_lines.animate.move_to(ORIGIN))
        
        # 2. Add the smaller "Operation A" label
        operation_a_label = Text("Operation A", font_size=36).next_to(code_lines, UP)
        self.play(Write(operation_a_label))

        self.wait(3)
