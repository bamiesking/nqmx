from manim import (
    DoubleArrow,
    ApplyMethod,
    ZoomedScene,
    Tex,
    Transform,
    SVGMobject,
    RIGHT,
    UR,
    UL,
    DOWN,
    VGroup,
    Write,
    Unwrite,
    Homotopy,
    Text,
    MathTex,
    rate_functions,
    Succession,
    Wait,
    AnimationGroup,
    TransformMatchingTex,
    TexTemplate,
)


class WRLocking(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoomed_camera_frame_starting_position=(-2.75, 0, 0),
            zoom_factor=0.5,
            zoomed_display_height=5,
            zoomed_display_width=5,
            zoomed_display_center=0,
            **kwargs,
        )

    def construct(self):
        cmTemplate = TexTemplate()
        cmTemplate.add_to_preamble(r"\usepackage{cmbright}")
        self.camera.background_color = "white"

        def clock_evolve(x, y, z, t):
            v = 4e1 * 0.98
            return (x - v * t, y, z)

        def clock_shift(x_shift, y_shift, z_shift):
            def func(x, y, z, t):
                return (
                    x - x_shift * t,
                    y - y_shift * t,
                    z - z_shift * t,
                )

            return func

        def create_clock(color, width=7, length=5):
            g = VGroup()
            clk_prev = SVGMobject("clock.svg", stroke_color=color, stroke_width=width)
            g.add(clk_prev)
            for i in range(length):
                clk = SVGMobject("clock.svg", stroke_color=color, stroke_width=width)
                clk.next_to(clk_prev, RIGHT, buff=-0.02)
                g.add(clk)
                clk_prev = clk
            return g

        m = create_clock("#4495d9")
        m.set_y(1.5)
        s = create_clock("#d99144")
        s.set_y(-1.5)

        free_running_tex = MathTex(
            r"f_1 \approx f_2",
            substrings_to_isolate=["f_1", r"\approx", "f_2"],
        ).to_edge(UR)
        free_running_tex.set_color_by_tex("f_1", "#4495d9")
        free_running_tex.set_color_by_tex(r"\approx", "black")
        free_running_tex.set_color_by_tex("f_2", "#d99144")

        syntonisation_tex = MathTex(
            r"f_1 = f_2",
            substrings_to_isolate=["f_1", "=", "f_2"],
        ).to_edge(UR)
        syntonisation_tex.set_color_by_tex("f_1", "#4495d9")
        syntonisation_tex.set_color_by_tex(r"=", "black")
        syntonisation_tex.set_color_by_tex("f_2", "#d99144")
        (ApplyMethod,)

        label = Tex(
            "Free-running oscillators", color="black", tex_template=cmTemplate
        ).to_edge(UL)
        syntonisation_label = Tex(
            "Syntonisation", color="black", tex_template=cmTemplate
        ).to_edge(UL)
        coarse_sync_label = Tex(
            "Coarse synchronisation", color="black", tex_template=cmTemplate
        ).to_edge(UL)
        fine_sync_label = Tex(
            "Fine synchronisation", color="black", tex_template=cmTemplate
        ).to_edge(UL)

        coarse_sync_tex = MathTex(
            r"\Delta t < 1~\mu s", substrings_to_isolate=[r"\mu s"], color="black"
        ).next_to(syntonisation_tex, DOWN)

        fine_sync_tex = MathTex(
            r"\Delta t < 1~ns", substrings_to_isolate=[r"ns"], color="black"
        ).next_to(syntonisation_tex, DOWN)

        def update_text(text):
            def func(mobject):
                mobject.become(Text(text))
                return mobject

            return func

        self.play(
            Write(m[0], reverse=False, run_time=2),
            Write(s[0], reverse=False, run_time=2),
        )
        self.play(
            Succession(
                Write(label, run_time=1),
                # Write(label.to_edge(UL)),
                AnimationGroup(
                    Homotopy(
                        homotopy=clock_evolve,
                        mobject=s,
                        rate_func=rate_functions.ease_out_quad,
                        run_time=7,
                        replace_mobject_with_target_in_scene=True,
                    ),
                    Succession(
                        Write(free_running_tex),
                        Wait(3.5),
                        Unwrite(label, run_time=1),
                        # Write(syntonisation_label.to_edge(UL)),
                    ),
                ),
            ),
        )
        deltaphi_arrow_before_coarse = DoubleArrow(
            start=(-4.6, 0, 0), end=(-0.1, 0, 0), color="black"
        ).scale(0.5, scale_tips=True)
        deltaphi_tex_before_coarse = MathTex(r"\Delta t", color="black").move_to(
            (-2.35, -0.5, 0)
        )

        deltaphi_arrow = DoubleArrow(
            start=(-4.2, 0, 0), end=(-1.3, 0, 0), color="black"
        ).scale(0.5, scale_tips=True)
        deltaphi_tex = MathTex(r"\Delta t", color="black").move_to((-2.75, -0.5, 0))

        self.play(
            Succession(
                Write(syntonisation_label, run_time=1),
                TransformMatchingTex(free_running_tex, syntonisation_tex),
                AnimationGroup(
                    Homotopy(
                        homotopy=clock_shift(0, -1.5, 0),
                        mobject=s,
                        rate_func=rate_functions.linear,
                        run_time=1,
                        replace_mobject_with_target_in_scene=True,
                    ),
                    Homotopy(
                        homotopy=clock_shift(0, 1.5, 0),
                        mobject=m,
                        rate_func=rate_functions.linear,
                        run_time=1,
                        replace_mobject_with_target_in_scene=True,
                    ),
                ),
                Wait(1),
                Unwrite(syntonisation_label, run_time=1),
                Wait(1),
            ),
        )
        # coarse_sync_label = MarkupText("Coarse synchronisation")
        # self.play(Succession(Unwrite(syntonisation_label), Write(coarse_sync_label)))

        self.play(
            Succession(
                Write(coarse_sync_label, run_time=1),
                Write(deltaphi_arrow_before_coarse),
                Write(deltaphi_tex_before_coarse),
                Write(coarse_sync_tex),
            ),
        )
        self.play(
            Succession(
                AnimationGroup(
                    s.animate.shift((-0.75, 0, 0)),
                    Transform(deltaphi_arrow_before_coarse, deltaphi_arrow),
                    Transform(deltaphi_tex_before_coarse, deltaphi_tex),
                ),
                Wait(1),
                Unwrite(coarse_sync_label, run_time=1),
                Wait(1),
            )
        )
        self.play(
            Succession(
                Write(fine_sync_label, run_time=1),
                Wait(1),
                AnimationGroup(
                    Unwrite(deltaphi_tex_before_coarse),
                    Unwrite(deltaphi_arrow_before_coarse),
                ),
                s.animate.shift((-1.4, 0, 0)),
                Transform(coarse_sync_tex, fine_sync_tex),
            )
        )
