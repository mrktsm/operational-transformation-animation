from manim import *
from manim.utils.space_ops import angle_of_vector
import numpy as np

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
        # For "hello world", 'w' is at index 5 because of a space in the animation. The slice should be up to 11.
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

        self.wait(1)

        # 3. Create Operation B with the same operations as ComplexTransformation
        ops_list_b = VGroup(
            MarkupText(f'<span foreground="{purple}">delete</span><span foreground="{yellow}">(</span><span foreground="{number_color}">1</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"H"</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">5</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">delete</span><span foreground="{yellow}">(</span><span foreground="{number_color}">1</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"W"</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size),
            MarkupText(f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">5</span><span foreground="{yellow}">);</span>', font="Monospace", font_size=code_font_size)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        # 4. Create Operation B label
        operation_b_label = Text("Operation B", font_size=36).next_to(ops_list_b, UP)
        operation_b_group = VGroup(ops_list_b, operation_b_label)
        
        # 5. Move Operation A left while Operation B slides in from the right simultaneously
        operation_a_group = VGroup(code_lines, operation_a_label)
        
        # Position Operation B way off-screen to the right initially
        operation_b_group.move_to(RIGHT * 8)  # Much further off-screen
        operation_b_group.set_opacity(0)  # Start invisible for fade-in effect
        
        # Add Operation B to the scene (invisible and off-screen)
        self.add(operation_b_group)
        
        # Animate both movements simultaneously with fade-in
        self.play(
            operation_a_group.animate.move_to(LEFT * 2),
            operation_b_group.animate.move_to(RIGHT * 2).set_opacity(1),
            run_time=1.5
        )
        
        self.wait(0.5)
        
        # Highlight the last retain(5) operation in Operation B
        last_retain = ops_list_b[5]  # The last operation is retain(5)
        retain_highlight = SurroundingRectangle(last_retain, color=YELLOW, stroke_width=2, buff=0.1)
        self.play(Create(retain_highlight))
        self.wait(1)
        self.play(FadeOut(retain_highlight))
        
        self.wait(0.5)
        
        # 7. Add the dot operator
        dot_operator = Text("•", font_size=36).move_to((operation_a_group.get_right()[0] + operation_b_group.get_left()[0]) / 2, UP * 0)
        
        self.play(Write(dot_operator), run_time=0.5)
        self.wait(0.5)
        
        # 9. Collapse operations to labels and move directly to final centered positions
        # Create the equals sign and result elements
        equals_sign = Text("=", font_size=36)
        hello_world_result = Text("Hello World", font_size=36)
        
        # Create a temporary group to calculate final positions
        temp_equation = VGroup(operation_a_label.copy(), dot_operator.copy(), operation_b_label.copy(), equals_sign, hello_world_result)
        temp_equation.arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        
        # Get the final target positions for each element
        final_a_pos = temp_equation[0].get_center()
        final_dot_pos = temp_equation[1].get_center()
        final_b_pos = temp_equation[2].get_center()
        
        # Animate: fade out detailed instructions and move labels to final positions
        self.play(
            FadeOut(code_lines),
            FadeOut(ops_list_b),
            operation_a_label.animate.move_to(final_a_pos),
            operation_b_label.animate.move_to(final_b_pos),
            dot_operator.animate.move_to(final_dot_pos),
            run_time=1.5
        )
        self.wait(0.3)
        
        # 10. Animate the equals sign and result appearing in their final positions
        equals_sign.move_to(temp_equation[3].get_center())
        hello_world_result.move_to(temp_equation[4].get_center())
        
        self.play(Write(equals_sign), run_time=0.5)
        self.wait(0.3)
        self.play(Write(hello_world_result), run_time=0.8)
        
        self.wait(3)

        # 11. Fade out the entire equation
        final_equation_group = VGroup(operation_a_label, dot_operator, operation_b_label, equals_sign, hello_world_result)
        self.play(FadeOut(final_equation_group), run_time=1)
        self.wait(1)


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
        # 1. Define the same color scheme as used in other scenes
        purple = "#C586C0"
        yellow = "#FFD700"
        string_color = "#CE9178"
        number_color = "#569CD6"
        
        # 2. Define points for a perfect diamond shape, centered at the origin
        v_dist = 2.5
        h_dist = 3.5
        top_point = UP * v_dist
        bottom_point = DOWN * v_dist
        left_point = LEFT * h_dist
        right_point = RIGHT * h_dist
        
        # 3. Create the top arrows
        arrow_b = Arrow(top_point, left_point, buff=0, color="#2366D1")
        arrow_a = Arrow(top_point, right_point, buff=0, color="#903F32")

        # 4. Create the labels for the arrows
        label_b = Text("b", color="#2366D1", font_size=30).move_to(arrow_b.get_center() + UL * 0.3)
        label_a = Text("a", color="#903F32", font_size=30).move_to(arrow_a.get_center() + UR * 0.3)

        # 5. Animate top part
        self.play(GrowArrow(arrow_b), GrowArrow(arrow_a))
        self.play(Write(label_b), Write(label_a))
        self.wait(0.5)

        # 6. Make origin dot appear briefly and disappear
        origin_dot = Dot(top_point, color=GREEN, radius=0.1125)
        self.play(FadeIn(origin_dot), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(origin_dot), run_time=0.5)
        self.wait(0.5)

        # 7. Prepare all bottom objects but DO NOT add or animate them yet!
        dashed_line_1 = DashedLine(left_point, bottom_point, color="#444444")
        dashed_line_2 = DashedLine(right_point, bottom_point, color="#444444")
        arrow_head_1 = Arrow(
            left_point, bottom_point,
            color="#444444",
            stroke_opacity=0,
            tip_length=0.35,
            buff=0
        )
        arrow_head_2 = Arrow(
            right_point, bottom_point,
            color="#444444",
            stroke_opacity=0,
            tip_length=0.35,
            buff=0
        )
        arrow_a_prime = Arrow(arrow_a.get_center(), dashed_line_1.get_center(), buff=0, color="#D64B3D")
        arrow_b_prime = Arrow(arrow_b.get_center(), dashed_line_2.get_center(), buff=0, color="#2366D1")
        label_a_prime = Text("a'", color="#D64B3D", font_size=30).next_to(arrow_a_prime.get_end(), DL, buff=0.15)
        label_b_prime = Text("b'", color="#2366D1", font_size=30).next_to(arrow_b_prime.get_end(), DR, buff=0.15)

        # 8. Animate all at once
        self.play(
            FadeIn(dashed_line_1),
            FadeIn(dashed_line_2),
            FadeIn(arrow_head_1),
            FadeIn(arrow_head_2),
            GrowArrow(arrow_a_prime),
            GrowArrow(arrow_b_prime),
            Write(label_a_prime),
            Write(label_b_prime),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(0.5)

        # 9. Fade out the inner arrows and labels
        self.play(
            FadeOut(arrow_a_prime),
            FadeOut(arrow_b_prime),
            FadeOut(label_a_prime),
            FadeOut(label_b_prime),
            run_time=1
        )
        self.wait(0.5)

        # 10. Display "go", "Client", and "Server" labels
        go_text = MarkupText(
            f'<span foreground="{string_color}">"go"</span>',
            font="Monospace", 
            font_size=24
        ).next_to(top_point, UP, buff=0.1)

        client_text = Text("CLIENT", font_size=32, color="#2366D1").next_to(go_text, LEFT, buff=1.5)
        server_text = Text("SERVER", font_size=32, color="#903F32").next_to(go_text, RIGHT, buff=1.5)

        self.play(
            Write(go_text),
            Write(client_text),
            Write(server_text),
            run_time=1
        )
        self.wait(1)
        
        # 11. Add operation sequences next to the b and a labels
        # Left operations (next to "b")
        left_ops = VGroup(
            MarkupText(
                f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">2</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=16
            ),
            MarkupText(
                f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"a"</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=16
            )
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(label_b, LEFT, buff=0.3)
        
        # Right operations (next to "a")
        right_ops = VGroup(
            MarkupText(
                f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">2</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=16
            ),
            MarkupText(
                f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"t"</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=16
            )
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(label_a, RIGHT, buff=0.3)
        
        # Animate the operations appearing
        self.play(Write(left_ops), Write(right_ops), run_time=1)
        self.wait(2)

        # 12. Display the result at the bottom
        result_text = MarkupText(
            f'<span foreground="{string_color}">"gota"</span> or <span foreground="{string_color}">"goat"</span>',
            font="Monospace",
            font_size=20
        ).next_to(bottom_point, DOWN, buff=0.3)
        self.play(Write(result_text))
        self.wait(2)

        # Fade out the temporary result before sending ops to server
        self.play(FadeOut(result_text), run_time=0.5)
        self.wait(0.2)

        # 13. Animate copies of the operations flying to the server
        left_ops_copy = left_ops.copy()
        right_ops_copy = right_ops.copy()
        self.play(
            FadeOut(left_ops_copy, target_position=server_text.get_center(), scale=0.5),
            FadeOut(right_ops_copy, target_position=server_text.get_center(), scale=0.5),
            run_time=1.5
        )
        self.wait(2)

        # 14. Server "spits out" transformed operations a' and b' with their labels
        a_prime_ops = VGroup(
            MarkupText(
                f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">2</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=16
            ),
            MarkupText(
                f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"a"</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=16
            ),
            MarkupText(
                f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">1</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=16
            )
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        b_prime_ops = VGroup(
            MarkupText(
                f'<span foreground="{purple}">retain</span><span foreground="{yellow}">(</span><span foreground="{number_color}">3</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=16
            ),
            MarkupText(
                f'<span foreground="{purple}">insert</span><span foreground="{yellow}">(</span><span foreground="{string_color}">"t"</span><span foreground="{yellow}">);</span>',
                font="Monospace", font_size=16
            )
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        # Create and position the a' and b' labels
        label_a_prime_new = Text("a'", color="#D64B3D", font_size=30).next_to(dashed_line_1.get_center(), DL, buff=0.15)
        label_b_prime_new = Text("b'", color="#2366D1", font_size=30).next_to(dashed_line_2.get_center(), DR, buff=0.15)
        
        # Position the operations next to their labels
        a_prime_ops.next_to(label_a_prime_new, LEFT, buff=0.3)
        b_prime_ops.next_to(label_b_prime_new, RIGHT, buff=0.3)

        # Group them for animation
        a_prime_full_group = VGroup(label_a_prime_new, a_prime_ops)
        b_prime_full_group = VGroup(label_b_prime_new, b_prime_ops)

        # Animate them appearing from the server
        self.play(
            GrowFromPoint(a_prime_full_group, server_text.get_center()),
            GrowFromPoint(b_prime_full_group, server_text.get_center()),
            run_time=1.5
        )
        self.wait(2)

        # 15. Display the final, converged result
        final_result_text = MarkupText(
            f'<span foreground="{string_color}">"goat"</span>',
            font="Monospace",
            font_size=20
        ).next_to(bottom_point, DOWN, buff=0.3)
        self.play(Write(final_result_text))
        self.wait(2)

        # 16. Clear everything except the top part of the diagram
        self.play(
            FadeOut(go_text),
            FadeOut(left_ops),
            FadeOut(right_ops),
            FadeOut(dashed_line_1),
            FadeOut(dashed_line_2),
            FadeOut(arrow_head_1),
            FadeOut(arrow_head_2),
            FadeOut(a_prime_full_group),
            FadeOut(b_prime_full_group),
            FadeOut(final_result_text),
            run_time=1.5
        )
        self.wait(2)

        # 17. Scale and shift the diagram to make space
        # Store original vectors before scaling
        unscaled_b_vector = arrow_b.get_end() - arrow_b.get_start()
        unscaled_a_vector = arrow_a.get_end() - arrow_a.get_start()

        diagram_top_group = VGroup(
            client_text, server_text, 
            arrow_a, label_a, 
            arrow_b, label_b
        )
        self.play(
            diagram_top_group.animate.scale(0.8).shift(UP * 0.5 + RIGHT * 1), 
            run_time=1
        )
        self.wait(0.5)

        # Get the scaled visual properties from the original arrows
        scaled_blue_stroke_width = arrow_b.get_stroke_width()
        scaled_blue_tip_length = arrow_b.tip.get_length()
        scaled_red_stroke_width = arrow_a.get_stroke_width()
        scaled_red_tip_length = arrow_a.tip.get_length()

        # 18. Draw arrow 'c' extending from arrow 'b'
        scale_factor = 0.8
        start_c = arrow_b.get_end()
        end_c = start_c + unscaled_b_vector * scale_factor
        arrow_c = Arrow(
            start_c, end_c, buff=0, color="#2366D1",
            stroke_width=scaled_blue_stroke_width,
            tip_length=scaled_blue_tip_length
        )
        label_c = Text("c", color="#2366D1", font_size=24).move_to(arrow_c.get_center() + UL * 0.3)

        self.play(GrowArrow(arrow_c), Write(label_c))
        self.wait(1)

        # 19. Draw a dotted red line through the intersection of blue arrows, parallel to red arrow
        # Find the intersection point of the two blue arrows
        intersection_point = arrow_b.get_end()  # This is where arrow_b ends and arrow_c starts
        
        # Get the direction vector of the red arrow
        red_direction = arrow_a.get_end() - arrow_a.get_start()
        
        # Create start and end points for the dotted line (extend in both directions)
        line_length = np.linalg.norm(red_direction) * 1.5  # Make it a bit longer
        normalized_direction = red_direction / np.linalg.norm(red_direction)
        
        dotted_line_start = intersection_point - normalized_direction * line_length / 2
        dotted_line_end = intersection_point + normalized_direction * line_length / 2
        
        dotted_red_line = DashedLine(dotted_line_start, dotted_line_end, color="#903F32", dash_length=0.1)
        
        self.play(Create(dotted_red_line))
        self.wait(2)

        # 20. Make the dotted red line disappear
        self.play(FadeOut(dotted_red_line))
        self.wait(0.5)

        # 21. Draw a blue arrow from the end of the red arrow, parallel to blue arrows
        # Start from the end of the red arrow
        start_b_prime = arrow_a.get_end()
        
        # Use the scaled direction vector of the blue arrows (arrow_b)
        end_b_prime = start_b_prime + unscaled_b_vector * scale_factor
        
        # Create the blue arrow and label
        arrow_b_prime = Arrow(
            start_b_prime, end_b_prime, buff=0, color="#2366D1",
            stroke_width=scaled_blue_stroke_width,
            tip_length=scaled_blue_tip_length
        )
        label_b_prime = Text("b'", color="#2366D1", font_size=24).move_to(arrow_b_prime.get_center() + DOWN * 0.5)
        
        self.play(GrowArrow(arrow_b_prime), Write(label_b_prime))
        self.wait(1)

        # 22. Draw a temporary dotted blue arrow
        # Start from the end of the b' arrow
        start_dotted_blue = arrow_b_prime.get_end()
        # Use the scaled direction vector of arrow c (which is same as b)
        end_dotted_blue = start_dotted_blue + unscaled_b_vector * scale_factor
        # Create the dotted blue arrow (no label)
        dotted_blue_arrow = DashedVMobject(
            Arrow(
                start_dotted_blue, end_dotted_blue, buff=0, color="#2366D1",
                stroke_width=scaled_blue_stroke_width,
                tip_length=scaled_blue_tip_length
            )
        )
        self.play(FadeIn(dotted_blue_arrow, run_time=1))
        self.wait(1)
        self.play(FadeOut(dotted_blue_arrow, run_time=1))
        self.wait(0.5)

        # 23. Draw a red arrow a' to complete the parallelogram
        # It starts from the intersection of b and c
        start_a_prime = arrow_b.get_end()
        # It points to the end of the b' arrow, using the scaled vector for a
        end_a_prime = start_a_prime + unscaled_a_vector * scale_factor
        # Create the red arrow and label a'
        arrow_a_prime_final = Arrow(
            start_a_prime, end_a_prime, buff=0, color="#903F32",
            stroke_width=scaled_red_stroke_width,
            tip_length=scaled_red_tip_length
        )
        label_a_prime_final = Text("a'", color="#903F32", font_size=24).move_to(arrow_a_prime_final.get_center() + DOWN * 0.5)
        self.play(GrowArrow(arrow_a_prime_final), Write(label_a_prime_final))
        self.wait(1)
        
        # 24. Draw a solid blue arrow c' where the dotted arrow was
        # Start from the end of the b' arrow
        start_c_prime_arrow = arrow_b_prime.get_end()
        # Use the scaled direction vector of arrow c (which is same as b)
        end_c_prime_arrow = start_c_prime_arrow + unscaled_b_vector * scale_factor
        # Create the solid blue arrow and label c'
        arrow_c_prime = Arrow(
            start_c_prime_arrow, end_c_prime_arrow, buff=0, color="#2366D1",
            stroke_width=scaled_blue_stroke_width,
            tip_length=scaled_blue_tip_length
        )
        label_c_prime = Text("c'", color="#2366D1", font_size=24).move_to(arrow_c_prime.get_center() + DOWN * 0.5)
        self.play(GrowArrow(arrow_c_prime), Write(label_c_prime))
        self.wait(1)

        # 25. Draw arrow a'' from the end of c, parallel to a'
        start_a_double_prime = arrow_c.get_end()
        end_a_double_prime = start_a_double_prime + unscaled_a_vector * scale_factor

        arrow_a_double_prime = Arrow(
            start_a_double_prime, end_a_double_prime, buff=0, color="#903F32",
            stroke_width=scaled_red_stroke_width,
            tip_length=scaled_red_tip_length
        )
        label_a_double_prime = Text("a''", color="#903F32", font_size=24).move_to(arrow_a_double_prime.get_center() + DOWN * 0.5)

        self.play(GrowArrow(arrow_a_double_prime), Write(label_a_double_prime))
        self.wait(5)
