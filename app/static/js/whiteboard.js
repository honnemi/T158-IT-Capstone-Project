const whiteboardElement = document.getElementById("whiteboard");
const whiteboardContainer = document.getElementById("whiteboard-container");

if (whiteboardElement && whiteboardContainer) {
  let currentColour = "#1F2937";
  let currentBrushSize = 3;
  let arrowCleanup = null;
  let eraserHandler = null;
  let saveTimeout;

  const canvas = new fabric.Canvas("whiteboard", {
    backgroundColor: "#ffffff",
    selection: true,
  });

  const brushSizeControl = document.getElementById("brush-size-control");
  const brushSizeSlider = document.getElementById("brush-size");
  const brushSizeValue = document.getElementById("brush-size-value");
  const imageLoader = document.getElementById("image-loader");

  const tools = document.querySelectorAll(".tool");
  const colours = document.querySelectorAll(".colour");

  function resizeCanvas() {
    canvas.setDimensions({
      width: whiteboardContainer.clientWidth,
      height: whiteboardContainer.clientHeight,
    });

    canvas.requestRenderAll();
  }

  resizeCanvas();

  function setActiveTool(tool) {
    tools.forEach((button) => button.classList.remove("active"));
    tool.classList.add("active");
  }

  function clearArrowState() {
    if (arrowCleanup) {
      arrowCleanup();
      arrowCleanup = null;
    }
  }

  function clearEraserState() {
    if (eraserHandler) {
      canvas.off("mouse:down", eraserHandler);
      eraserHandler = null;
    }
  }

  function clearToolState() {
    clearArrowState();
    clearEraserState();

    canvas.isDrawingMode = false;
    canvas.selection = true;
    canvas.defaultCursor = "default";
    canvas.hoverCursor = "move";

    if (canvas.freeDrawingBrush) {
      canvas.freeDrawingBrush.color = currentColour;
      canvas.freeDrawingBrush.width = currentBrushSize;
    }
  }

  function activateEraserTool() {
    clearEraserState();

    canvas.isDrawingMode = false;
    canvas.selection = false;
    canvas.defaultCursor = "crosshair";
    canvas.hoverCursor = "crosshair";

    eraserHandler = function (options) {
      const target = options.target || canvas.findTarget(options.e);

      if (target) {
        canvas.remove(target);
        canvas.discardActiveObject();
        canvas.requestRenderAll();
      }
    };

    canvas.on("mouse:down", eraserHandler);
  }

  function createShape(shape) {
    let object;

    if (shape === "square") {
      object = new fabric.Rect({
        left: 100,
        top: 100,
        width: 100,
        height: 100,
        fill: "transparent",
        stroke: currentColour,
        strokeWidth: 3,
        strokeUniform: true,
      });
    }

    if (shape === "circle") {
      object = new fabric.Circle({
        left: 100,
        top: 100,
        radius: 50,
        fill: "transparent",
        stroke: currentColour,
        strokeWidth: 3,
        strokeUniform: true,
      });
    }

    if (shape === "text") {
      object = new fabric.IText("Text", {
        left: 100,
        top: 100,
        fill: currentColour,
        fontSize: 24,
        fontFamily: "Arial",
      });
    }

    if (object) {
      canvas.add(object);
      canvas.setActiveObject(object);

      if (shape === "text") {
        object.enterEditing();
        object.selectAll();
      }

      canvas.requestRenderAll();
    }
  }

  function activateArrowTool() {
    let startX = 0;
    let startY = 0;
    let isDrawing = false;
    let previewLine = null;
    let previewHead = null;

    function removePreview() {
      if (previewLine) canvas.remove(previewLine);
      if (previewHead) canvas.remove(previewHead);

      previewLine = null;
      previewHead = null;
      isDrawing = false;

      canvas.requestRenderAll();
    }

    function mouseDown(options) {
      if (options.e.button !== 0) return;

      const pointer = canvas.getPointer(options.e);

      startX = pointer.x;
      startY = pointer.y;
      isDrawing = true;

      previewLine = new fabric.Line(
        [startX, startY, startX, startY],
        {
          stroke: currentColour,
          strokeWidth: 3,
          strokeLineCap: "round",
          selectable: false,
          evented: false,
        },
      );

      previewHead = new fabric.Triangle({
        left: startX,
        top: startY,
        originX: "center",
        originY: "center",
        width: 14,
        height: 16,
        fill: currentColour,
        stroke: currentColour,
        strokeWidth: 1,
        angle: 90,
        selectable: false,
        evented: false,
      });

      canvas.add(previewLine, previewHead);
    }

    function mouseMove(options) {
      if (!isDrawing || !previewLine || !previewHead) return;

      const pointer = canvas.getPointer(options.e);
      const dx = pointer.x - startX;
      const dy = pointer.y - startY;

      if (Math.hypot(dx, dy) < 1) return;

      const angle = Math.atan2(dy, dx);
      const angleDegrees = (angle * 180) / Math.PI;

      previewLine.set({
        x1: startX,
        y1: startY,
        x2: pointer.x,
        y2: pointer.y,
      });

      previewHead.set({
        left: pointer.x,
        top: pointer.y,
        angle: angleDegrees + 90,
      });

      previewLine.setCoords();
      previewHead.setCoords();

      canvas.requestRenderAll();
    }

    function mouseUp() {
      if (!isDrawing) return;

      const line = previewLine;
      const head = previewHead;

      if (line && head) {
        const x1 = line.x1;
        const y1 = line.y1;
        const x2 = line.x2;
        const y2 = line.y2;

        if (Math.hypot(x2 - x1, y2 - y1) >= 5) {
          const finalLine = new fabric.Line(
            [x1, y1, x2, y2],
            {
              stroke: currentColour,
              strokeWidth: 3,
              strokeLineCap: "round",
              strokeUniform: true,
              selectable: false,
              evented: false,
            },
          );

          const angle = Math.atan2(y2 - y1, x2 - x1);

          const arrowHead = new fabric.Triangle({
            left: x2,
            top: y2,
            originX: "center",
            originY: "center",
            width: 14,
            height: 16,
            fill: currentColour,
            stroke: currentColour,
            strokeWidth: 1,
            angle: (angle * 180) / Math.PI + 90,
            selectable: false,
            evented: false,
          });

          removePreview();

          const arrow = new fabric.Group(
            [finalLine, arrowHead],
            {
              selectable: true,
              evented: true,
              objectCaching: false,
            },
          );

          canvas.add(arrow);
          canvas.setActiveObject(arrow);
        } else {
          removePreview();
        }
      } else {
        removePreview();
      }

      previewLine = null;
      previewHead = null;

      canvas.requestRenderAll();
    }

    canvas.on("mouse:down", mouseDown);
    canvas.on("mouse:move", mouseMove);
    canvas.on("mouse:up", mouseUp);

    arrowCleanup = () => {
      canvas.off("mouse:down", mouseDown);
      canvas.off("mouse:move", mouseMove);
      canvas.off("mouse:up", mouseUp);
      removePreview();
    };
  }

  if (!viewOnly) {
    if (brushSizeControl) {
      ["pointerdown", "mousedown"].forEach((eventName) => {
        brushSizeControl.addEventListener(eventName, (event) => {
          event.stopPropagation();
        });
      });
    }

    if (brushSizeSlider) {
      ["pointerdown", "mousedown", "click"].forEach((eventName) => {
        brushSizeSlider.addEventListener(eventName, (event) => {
          event.stopPropagation();
        });
      });

      brushSizeSlider.addEventListener("input", () => {
        currentBrushSize = Number(brushSizeSlider.value);

        if (canvas.freeDrawingBrush) {
          canvas.freeDrawingBrush.width = currentBrushSize;
        }

        if (brushSizeValue) {
          brushSizeValue.textContent = `${currentBrushSize}px`;
        }
      });
    }

    tools.forEach((tool) => {
      tool.addEventListener("click", () => {
        clearToolState();
        setActiveTool(tool);

        if (brushSizeControl) {
          brushSizeControl.style.display =
            tool.id === "pen" ? "flex" : "none";
        }

        switch (tool.id) {
          case "pen":
            canvas.isDrawingMode = true;
            canvas.selection = false;

            if (!canvas.freeDrawingBrush) {
              canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
            }

            canvas.freeDrawingBrush.color = currentColour;
            canvas.freeDrawingBrush.width = currentBrushSize;
            break;

          case "eraser":
            activateEraserTool();
            break;

          case "square":
          case "circle":
          case "text":
            createShape(tool.id);
            break;

          case "arrow":
            canvas.selection = false;
            canvas.defaultCursor = "crosshair";
            activateArrowTool();
            break;

          case "image":
            if (imageLoader) imageLoader.click();
            break;
        }
      });
    });

    colours.forEach((colour) => {
      colour.addEventListener("click", () => {
        currentColour = colour.dataset.color;

        if (canvas.freeDrawingBrush) {
          canvas.freeDrawingBrush.color = currentColour;
        }

        colours.forEach((button) => button.classList.remove("active"));
        colour.classList.add("active");
      });
    });

    if (imageLoader) {
      imageLoader.addEventListener("change", (event) => {
        const file = event.target.files[0];

        if (!file) return;

        const reader = new FileReader();

        reader.onload = async (loadEvent) => {
          try {
            const image = await fabric.FabricImage.fromURL(
              loadEvent.target.result,
            );

            image.scaleToWidth(250);
            image.set({ left: 100, top: 100 });

            canvas.add(image);
            canvas.setActiveObject(image);
            canvas.requestRenderAll();
          } catch (error) {
            console.error("Failed to load image:", error);
          }
        };

        reader.readAsDataURL(file);
        imageLoader.value = "";
      });
    }
  }

  if (typeof savedWhiteboard !== "undefined" && savedWhiteboard) {
    canvas
      .loadFromJSON(savedWhiteboard)
      .then(() => {
        if (viewOnly) {
          canvas.isDrawingMode = false;
          canvas.selection = false;

          canvas.forEachObject((object) => {
            object.selectable = false;
            object.evented = false;
          });

          canvas.discardActiveObject();
        }

        canvas.requestRenderAll();
      })
      .catch((error) => {
        console.error("Failed to load whiteboard:", error);
      });
  }

  if (!viewOnly) {
    function saveWhiteboard() {
      clearTimeout(saveTimeout);

      saveTimeout = setTimeout(() => {
        fetch(saveWhiteboardUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            whiteboard: JSON.stringify(canvas.toJSON()),
          }),
        }).catch((error) => {
          console.error("Failed to save whiteboard:", error);
        });
      }, 500);
    }

    canvas.on("object:added", saveWhiteboard);
    canvas.on("object:modified", saveWhiteboard);
    canvas.on("object:removed", saveWhiteboard);
    canvas.on("path:created", saveWhiteboard);
  }

  window.addEventListener("resize", resizeCanvas);
}