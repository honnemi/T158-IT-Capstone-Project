const whiteboardElement = document.getElementById("whiteboard");
const whiteboardContainer = document.getElementById("whiteboard-container");

if (whiteboardElement && whiteboardContainer) {
    let currentColour = "#1F2937";

    // Create canvas
    const canvas = new fabric.Canvas("whiteboard");

    // Set canvas dimensions
    canvas.setDimensions({
        width: whiteboardContainer.clientWidth,
        height: whiteboardContainer.clientHeight
    });

    // Save whiteboard as JSON and return to route
    let saveTimeout;

    function saveWhiteboard() {
        const whiteboardData = JSON.stringify(canvas.toJSON());

        fetch(saveWhiteboardUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                whiteboard: whiteboardData
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Save failed: ${response.status}`);
            }

            return response.json();
        })
        .then(data => {
            console.log("Whiteboard saved:", data);
        })
        .catch(error => {
            console.error("Failed to save whiteboard:", error);
        });
    }

    // Delay saves slightly so requests aren't so frequent
    function scheduleSave() {
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(saveWhiteboard, 500);
    }

    // Set pen properties
    canvas.isDrawingMode = false;
    canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
    canvas.freeDrawingBrush.width = 3;
    canvas.freeDrawingBrush.color = currentColour;

    // Track tool states
    let isArrowModeActive = false;
    let isDrawingArrow = false;

    let line;
    let arrowhead;
    
    // Reset tool states on tool toggle
    function clearToolState() {
        isArrowModeActive = false;
        isDrawingArrow = false;
        line = null;
        arrowhead = null;

        canvas.isDrawingMode = false;
        canvas.selection = true;
        canvas.defaultCursor = "default";
    }

    const tools = document.querySelectorAll(".tool");

    // Tool toggle
    tools.forEach(tool => {
        tool.addEventListener("click", () => {
            tools.forEach(t => t.classList.remove("active"));
            tool.classList.add("active");
            clearToolState();
        });
    });
    
    // Colour swatches
    const colourButtons = document.querySelectorAll(".colour");

    colourButtons.forEach(button => {
        button.addEventListener("click", () => {
            colourButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            currentColour = button.dataset.color;

            if (canvas.freeDrawingBrush) {
                canvas.freeDrawingBrush.color = currentColour;
            }
        });
    });

    // Pen tool
    const penButton = document.getElementById("pen");

    if (penButton) {
        penButton.addEventListener("click", () => {
            canvas.isDrawingMode = true;
            canvas.freeDrawingBrush.color = currentColour;
            canvas.freeDrawingBrush.width = 3;
        });
    }

    // Erase tool
    const eraserButton = document.getElementById("eraser");

    if (eraserButton) {
        eraserButton.addEventListener("click", () => {
            clearToolState();

            const activeObjects = canvas.getActiveObjects();

            if (activeObjects.length > 0) {
                activeObjects.forEach(object => {
                    canvas.remove(object);
                });

                canvas.discardActiveObject();
                canvas.requestRenderAll();
            }
        });
    }

    // Square tool
    const squareButton = document.getElementById("square");

    if (squareButton) {
        squareButton.addEventListener("click", () => {
            const rectangle = new fabric.Rect({
                left: 100,
                top: 100,
                width: 100,
                height: 100,
                fill: "transparent",
                stroke: currentColour,
                strokeWidth: 2,
                strokeUniform: true
            });

            canvas.add(rectangle);
            canvas.setActiveObject(rectangle);
            canvas.renderAll();
        });
    }

    // Circle tool
    const circleButton = document.getElementById("circle");

    if (circleButton) {
        circleButton.addEventListener("click", () => {
            const circle = new fabric.Ellipse({
                left: 100,
                top: 100,
                rx: 50,
                ry: 50,
                fill: "transparent",
                stroke: currentColour,
                strokeWidth: 2,
                strokeUniform: true
            });

            canvas.add(circle);
            canvas.setActiveObject(circle);
            canvas.renderAll();
        });
    }

    // Text tool
    const textButton = document.getElementById("text");

    if (textButton) {
        textButton.addEventListener("click", () => {
            const text = new fabric.IText("Text", {
                left: 100,
                top: 100,
                fontSize: 20,
                fill: currentColour,
                fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif'
            });

            canvas.add(text);
            canvas.setActiveObject(text);
            text.enterEditing();
            canvas.renderAll();
        });
    }

    // Arrow tool
    const arrowButton = document.getElementById("arrow");

    if (arrowButton) {
        arrowButton.addEventListener("click", () => {
            isArrowModeActive = true;
            canvas.selection = false;
            canvas.defaultCursor = "crosshair";
        });
    }

    canvas.on("mouse:down", options => {
        if (!isArrowModeActive || options.target) return;

        isDrawingArrow = true;

        const pointer = canvas.getPointer(options.e);
        const color = currentColour;

        line = new fabric.Line(
            [pointer.x, pointer.y, pointer.x, pointer.y],
            {
                strokeWidth: 3,
                stroke: color,
                fill: "transparent",
                originX: "center",
                originY: "center",
                selectable: false,
                hoverCursor: "default"
            }
        );

        arrowhead = new fabric.Triangle({
            width: 15,
            height: 15,
            fill: color,
            left: pointer.x,
            top: pointer.y,
            originX: "center",
            originY: "center",
            selectable: false,
            angle: 0,
            hoverCursor: "default"
        });

        canvas.add(line, arrowhead);
    });

    canvas.on("mouse:move", options => {
        if (!isDrawingArrow || !line || !arrowhead) return;

        const pointer = canvas.getPointer(options.e);

        line.set({
            x2: pointer.x,
            y2: pointer.y
        });

        const dx = pointer.x - line.x1;
        const dy = pointer.y - line.y1;

        let angle = Math.atan2(dy, dx) * (180 / Math.PI);
        angle += 90;

        arrowhead.set({
            left: pointer.x,
            top: pointer.y,
            angle: angle
        });

        canvas.renderAll();
    });

    canvas.on("mouse:up", () => {
        if (!isDrawingArrow) return;

        isDrawingArrow = false;

        if (line && arrowhead) {
            const dx = line.x2 - line.x1;
            const dy = line.y2 - line.y1;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 5) {
                canvas.remove(line, arrowhead);
            } else {
                const arrowGroup = new fabric.Group([line, arrowhead], {
                    selectable: true,
                    hasBorders: true,
                    hasControls: true
                });

                canvas.remove(line, arrowhead);
                canvas.add(arrowGroup);

                arrowGroup.setCoords();
                canvas.setActiveObject(arrowGroup);
            }
        }

        line = null;
        arrowhead = null;
        canvas.renderAll();
    });

    // Image tool
    const imageToolBtn = document.getElementById("image");
    const imageLoader = document.getElementById("image-loader");

    if (imageToolBtn && imageLoader) {
        imageToolBtn.addEventListener("click", () => {
            imageLoader.click();
        });

        imageLoader.addEventListener("change", function(e) {
            const file = e.target.files[0];

            if (!file) return;

            const reader = new FileReader();

            reader.onload = function(event) {
                const imgDataUrl = event.target.result;

                fabric.Image.fromURL(imgDataUrl).then(fabricImg => {
                    const maxDimension =
                        Math.min(canvas.width, canvas.height) * 0.6;

                    if (
                        fabricImg.width > maxDimension ||
                        fabricImg.height > maxDimension
                    ) {
                        fabricImg.scaleToWidth(maxDimension);
                    }

                    fabricImg.set({
                        left:
                            canvas.width / 2 -
                            fabricImg.getScaledWidth() / 2,
                        top:
                            canvas.height / 2 -
                            fabricImg.getScaledHeight() / 2,
                        cornerColor: "#3B82F6",
                        cornerStrokeColor: "#1E40AF",
                        transparentCorners: false,
                        cornerSize: 10
                    });

                    canvas.add(fabricImg);
                    canvas.setActiveObject(fabricImg);
                    canvas.requestRenderAll();
                });
            };

            reader.readAsDataURL(file);
            this.value = "";
        });
    }

    // Load whiteboard and listen for events
    setTimeout(() => {
        canvas.setDimensions({
            width: whiteboardContainer.clientWidth,
            height: whiteboardContainer.clientHeight
        });

        if (savedWhiteboard) {
            try {
                const whiteboardData =
                    typeof savedWhiteboard === "string"
                        ? JSON.parse(savedWhiteboard)
                        : savedWhiteboard;

                canvas.loadFromJSON(whiteboardData, () => {
                    canvas.calcOffset();
                    canvas.requestRenderAll();

                    canvas.on("object:added", scheduleSave);
                    canvas.on("object:modified", scheduleSave);
                    canvas.on("object:removed", scheduleSave);
                });
            } catch (error) {
                console.error("Error loading whiteboard:", error);
            }
        } else {
            canvas.on("object:added", scheduleSave);
            canvas.on("object:modified", scheduleSave);
            canvas.on("object:removed", scheduleSave);
        }
    }, 100);
}