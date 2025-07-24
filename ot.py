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
        world_part = anim_doc_text[6:11]

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


class ComplexTransformation(Scene):
    def construct(self):
        # 1. Create and display the operations in the center
        code_font_size = 24 # Reduced from 30
        purple = "#C586C0"
        yellow = "#FFD700"
        string_color = "#CE9178"
        number_color = "#569CD6"

        ops_list = VGroup(
            MarkupText(f'<span foreground="{purple}">delete</span><span foreground="{yellow}">(</span><span foreground="{number_color}">1</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"H"</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">5</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">delete</span><span foreground="{yellow}">(</span><span foreground="{number_color}">1</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"W"</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">5</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        self.play(Write(ops_list))
        self.wait(1)

        # 2. Define the start and end text
        start_text = Text("hello world", font_size=36).to_edge(LEFT, buff=1)
        end_text = Text("Hello World", font_size=36).to_edge(RIGHT, buff=1)
        
        # 3. Animate everything appearing in a much quicker sequence
        self.play(Write(start_text), run_time=0.5)
        
        arrow1 = Arrow(start_text.get_right(), ops_list.get_left(), buff=0.2, stroke_width=3, tip_length=0.2)
        self.play(GrowArrow(arrow1), run_time=0.5)
        
        arrow2 = Arrow(ops_list.get_right(), end_text.get_left(), buff=0.2, stroke_width=3, tip_length=0.2)
        self.play(GrowArrow(arrow2), run_time=0.5)
        self.play(Write(end_text), run_time=0.5)
        
        self.wait(1) # Shortened wait

        # 4. Highlight the *last* retain(5) operation
        retain_operation = ops_list[5] # Index 5 is the new last operation
        highlight_box = SurroundingRectangle(retain_operation, color=YELLOW, buff=0.1)
        self.play(Create(highlight_box))
        self.wait(1)

        # 6. Clean up, resize, and add the final title
        self.play(
            FadeOut(start_text),
            FadeOut(end_text),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(highlight_box)
        )
        
        # Center and scale up the operations list
        self.play(ops_list.animate.scale(1.25).set_x(0))
        
        # Add the title above the now-centered operations
        operation_b_label = Text("Operation B", font_size=48).next_to(ops_list, UP)
        self.play(Write(operation_b_label))

        self.wait(3)


class Composition(Scene):
    def construct(self):
        # 1. Create and display the title
        title = Text("Composition").to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 2. Create the equation
        equation = MarkupText(
            '(Operation A ⋅ Operation B) = Hello World',
            font="Monospace",
            font_size=24 # Significantly reduced from 36
        )

        # 3. Create a more polished list of rules with the same font size
        rules = VGroup(
            Text("• Need to be in order", font_size=24),
            Text("• Must go through the same index", font_size=24),
            Text("• Not all operations can be combined", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        # 4. Group all content and center it on the screen
        content_group = VGroup(equation, rules).arrange(DOWN, buff=0.75)

        # 5. Animate the content appearing
        self.play(Write(equation))
        self.wait(1)
        self.play(FadeIn(rules, shift=UP*0.5))

        self.wait(3)


class DiamondDiagram(Scene):
    def construct(self):
        # 1. Define points for a perfect diamond shape, centered at the origin
        v_dist = 2.5
        h_dist = 3.5
        top_point = UP * v_dist
        bottom_point = DOWN * v_dist
        left_point = LEFT * h_dist
        right_point = RIGHT * h_dist
        
        # 2. Create the top arrows
        arrow_b = Arrow(top_point, left_point, buff=0)
        arrow_a = Arrow(top_point, right_point, buff=0)

        # 3. Create the labels for the arrows
        label_b = Text("b", color="#903F32").move_to(arrow_b.get_center() + UL * 0.3)
        label_a = Text("a", color="#903F32").move_to(arrow_a.get_center() + UR * 0.3)

        # 4. Animate top part
        self.play(GrowArrow(arrow_b), GrowArrow(arrow_a))
        self.play(Write(label_b), Write(label_a))
        self.wait(0.5)

        # 5. Blink origin dot
        origin_dot = Dot(top_point, color=YELLOW)
        self.play(Create(origin_dot))
        self.play(Blink(origin_dot, times=1, run_time=0.75))
        self.play(FadeOut(origin_dot))
        self.wait(0.5)

        # 6. Draw bottom part of the diagram
        dotted_line_1 = DashedLine(left_point, bottom_point)
        dotted_line_2 = DashedLine(right_point, bottom_point)
        self.play(Create(dotted_line_1), Create(dotted_line_2))
        self.wait(0.5)

        # Red crossed arrows
        arrow_a_prime = Arrow(arrow_a.get_center(), dotted_line_1.get_center(), buff=0, color="#D64B3D")
        arrow_b_prime = Arrow(arrow_b.get_center(), dotted_line_2.get_center(), buff=0, color="#D64B3D")
        self.play(GrowArrow(arrow_a_prime), GrowArrow(arrow_b_prime))
        
        # Labels for the new arrows
        label_a_prime = Text("a'", color="#D64B3D").next_to(arrow_a_prime.get_end(), DL, buff=0.15)
        label_b_prime = Text("b'", color="#D64B3D").next_to(arrow_b_prime.get_end(), DR, buff=0.15)
        self.play(Write(label_a_prime), Write(label_b_prime))

        self.wait(3)
