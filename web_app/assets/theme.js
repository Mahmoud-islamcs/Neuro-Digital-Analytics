(function () {
  const APPLY_DELAY_MS = 60;
  const SCROLL_THRESHOLD = 240;

  const PALETTES = {
    dark: {
      text: "#E6E9EF",
      textDim: "#9199A8",
      grid: "rgba(255, 255, 255, 0.06)",
      border: "rgba(255, 255, 255, 0.12)",
      menuBg: "#1C212E",
    },
    light: {
      text: "#172033",
      textDim: "#5D687B",
      grid: "rgba(17, 24, 39, 0.095)",
      border: "#D8E0EB",
      menuBg: "#FFFFFF",
    },
  };

  const CATEGORICAL_COLORWAY = [
    "#4C78A8",
    "#2CA7A0",
    "#E68A3C",
    "#8B7CC9",
    "#54A27A",
    "#D65F7A",
    "#E0B03D",
    "#6F71B5",
    "#4FB3C7",
    "#8C97A8",
  ];

  const SEQUENTIAL_COLORSCALES = {
    dark: [
      [0, "#12315A"],
      [0.25, "#20548C"],
      [0.5, "#3B79B5"],
      [0.75, "#6FA3D6"],
      [1, "#BFDCF5"],
    ],
    light: [
      [0, "#EAF2FF"],
      [0.25, "#BFD8F4"],
      [0.5, "#79A8D8"],
      [0.75, "#3F7DB6"],
      [1, "#1E4F82"],
    ],
  };

  function getShell() {
    return document.getElementById("app-shell");
  }

  function getTheme() {
    const shell = getShell();
    if (!shell) {
      return "dark";
    }
    return shell.classList.contains("theme-light") ? "light" : "dark";
  }

  function cssVar(name, fallback) {
    const shell = getShell() || document.documentElement;
    const value = window.getComputedStyle(shell).getPropertyValue(name).trim();
    return value || fallback;
  }

  function graphThemeLayout(theme) {
    const palette = PALETTES[theme] || PALETTES.dark;
    const text = cssVar("--text", palette.text);
    const textDim = cssVar("--text-dim", palette.textDim);
    const grid = cssVar("--grid", palette.grid);
    const border = cssVar("--surface-border", palette.border);
    const menuBg = cssVar("--menu-bg", palette.menuBg);

    return {
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      colorway: CATEGORICAL_COLORWAY,
      "font.color": text,
      "title.font.color": text,
      "legend.font.color": text,
      "xaxis.color": textDim,
      "xaxis.gridcolor": grid,
      "xaxis.zerolinecolor": grid,
      "xaxis.linecolor": grid,
      "yaxis.color": textDim,
      "yaxis.gridcolor": grid,
      "yaxis.zerolinecolor": grid,
      "yaxis.linecolor": grid,
      "polar.bgcolor": "rgba(0,0,0,0)",
      "polar.radialaxis.color": textDim,
      "polar.radialaxis.gridcolor": grid,
      "polar.angularaxis.color": textDim,
      "polar.angularaxis.gridcolor": grid,
      "scene.xaxis.color": textDim,
      "scene.xaxis.gridcolor": grid,
      "scene.yaxis.color": textDim,
      "scene.yaxis.gridcolor": grid,
      "scene.zaxis.color": textDim,
      "scene.zaxis.gridcolor": grid,
      "coloraxis.colorscale": SEQUENTIAL_COLORSCALES[theme] || SEQUENTIAL_COLORSCALES.dark,
      "hoverlabel.bgcolor": menuBg,
      "hoverlabel.bordercolor": border,
      "hoverlabel.font.color": text,
    };
  }

  function hasOutsideText(trace) {
    const position = trace && trace.textposition;
    if (Array.isArray(position)) {
      return position.some(function (value) {
        return String(value).indexOf("outside") !== -1;
      });
    }
    return String(position || "").indexOf("outside") !== -1;
  }

  function applyTraceTheme(graph, theme) {
    if (!graph || !window.Plotly || !graph.data) {
      return Promise.resolve();
    }

    const palette = PALETTES[theme] || PALETTES.dark;
    const text = cssVar("--text", palette.text);
    const promises = [];

    graph.data.forEach(function (trace, index) {
      const update = {};
      const outsideText = hasOutsideText(trace);

      if (outsideText) {
        if (!trace.textfont || trace.textfont.color !== text) {
          update["textfont.color"] = text;
        }
        if (!trace.outsidetextfont || trace.outsidetextfont.color !== text) {
          update["outsidetextfont.color"] = text;
        }
      }

      if (trace && trace.type === "parcats") {
        if (!trace.labelfont || trace.labelfont.color !== text) {
          update["labelfont.color"] = text;
        }
        if (!trace.tickfont || trace.tickfont.color !== text) {
          update["tickfont.color"] = text;
        }
      }

      if (Object.keys(update).length) {
        promises.push(window.Plotly.restyle(graph, update, [index]));
      }
    });

    return Promise.all(promises);
  }

  function applyAnnotationTheme(graph, theme) {
    if (!graph || !window.Plotly) {
      return Promise.resolve();
    }

    const palette = PALETTES[theme] || PALETTES.dark;
    const textDim = cssVar("--text-dim", palette.textDim);
    const annotations = (graph.layout && graph.layout.annotations) || [];
    const update = {};

    annotations.forEach(function (annotation, index) {
      if (!annotation.font || annotation.font.color !== textDim) {
        update["annotations[" + index + "].font.color"] = textDim;
      }
    });

    if (!Object.keys(update).length) {
      return Promise.resolve();
    }
    return window.Plotly.relayout(graph, update);
  }

  function applyGraphDetailsTheme(graph, theme) {
    return applyTraceTheme(graph, theme)
      .then(function () {
        return applyAnnotationTheme(graph, theme);
      });
  }

  function needsTheme(graph, layout, theme) {
    const fullLayout = graph && graph._fullLayout;
    if (!fullLayout) {
      return true;
    }
    return graph.__brainrotTheme !== theme ||
      !fullLayout.font ||
      fullLayout.font.color !== layout["font.color"];
  }

  function applyThemeToGraph(graph) {
    if (!graph || !window.Plotly || graph.__brainrotThemeApplying) {
      return;
    }

    const theme = getTheme();
    const layout = graphThemeLayout(theme);
    if (!needsTheme(graph, layout, theme)) {
      graph.__brainrotThemeApplying = true;
      applyGraphDetailsTheme(graph, theme)
        .then(function () {
          graph.__brainrotTheme = theme;
        })
        .catch(function () {})
        .finally(function () {
          graph.__brainrotThemeApplying = false;
        });
      return;
    }

    graph.__brainrotThemeApplying = true;
    window.Plotly.relayout(graph, layout)
      .then(function () {
        return applyGraphDetailsTheme(graph, theme);
      })
      .then(function () {
        graph.__brainrotTheme = theme;
      })
      .catch(function () {})
      .finally(function () {
        graph.__brainrotThemeApplying = false;
      });
  }

  function bindGraph(graph) {
    if (!graph || graph.__brainrotThemeBound) {
      return;
    }
    graph.__brainrotThemeBound = true;
    graph.on("plotly_afterplot", function () {
      window.setTimeout(function () {
        applyThemeToGraph(graph);
      }, APPLY_DELAY_MS);
    });
  }

  function syncDocumentTheme() {
    const theme = getTheme();
    document.documentElement.setAttribute("data-theme", theme);
    document.body.setAttribute("data-theme", theme);
  }

  function syncScrollControls() {
    const filterBar = document.querySelector(".filter-bar");
    const backToTop = document.getElementById("back-to-top");
    const isScrolled = window.scrollY > 8;
    const showBackToTop = window.scrollY > SCROLL_THRESHOLD;

    if (filterBar) {
      filterBar.classList.toggle("is-stuck", isScrolled);
    }
    if (backToTop) {
      backToTop.classList.toggle("is-visible", showBackToTop);
    }
  }

  function bindBackToTop() {
    const button = document.getElementById("back-to-top");
    if (!button || button.__brainrotBackToTopBound) {
      return;
    }
    button.__brainrotBackToTopBound = true;
    button.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  function applyThemeToAllGraphs() {
    syncDocumentTheme();
    bindBackToTop();
    syncScrollControls();
    document.querySelectorAll(".js-plotly-plot").forEach(function (graph) {
      bindGraph(graph);
      applyThemeToGraph(graph);
    });
  }

  function scheduleApply() {
    window.clearTimeout(window.__brainrotThemeTimer);
    window.__brainrotThemeTimer = window.setTimeout(applyThemeToAllGraphs, APPLY_DELAY_MS);
  }

  function observe() {
    const shell = getShell();
    if (!shell || window.__brainrotThemeObserver) {
      scheduleApply();
      return;
    }

    window.__brainrotThemeObserver = new MutationObserver(function (mutations) {
      const shouldApply = mutations.some(function (mutation) {
        return mutation.type === "childList" ||
          (mutation.type === "attributes" && mutation.attributeName === "class");
      });
      if (shouldApply) {
        scheduleApply();
      }
    });

    window.__brainrotThemeObserver.observe(shell, {
      attributes: true,
      attributeFilter: ["class"],
      childList: true,
      subtree: true,
    });
    scheduleApply();
  }

  window.addEventListener("scroll", syncScrollControls, { passive: true });
  window.addEventListener("resize", syncScrollControls);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", observe);
  } else {
    observe();
  }
})();
