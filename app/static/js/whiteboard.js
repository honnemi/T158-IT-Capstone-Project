const whiteboardElement = document.getElementById("whiteboard");
const whiteboardContainer = document.getElementById("whiteboard-container");

if (whiteboardElement && whiteboardContainer) {
    let currentColour = "#1F2937";
    let currentBrushSize = 3;

    const canvas = new fabric.Canvas("whiteboard");

    canvas.setDimensions({
        width: whiteboardContainer.clientWidth,
        height: whiteboardContainer.clientHeight
    });

    canvas.backgroundColor = "#ffffff";
    canvas.renderAll();

    const brushSizeControl = document.getElementById("brush-size-control");
    const brushSizeSlider = document.getElementById("brush-size");
    const brushSizeValue = document.getElementById("brush-size-value");

    const tools = document.querySelectorAll(".tool");
    const colours = document.querySelectorAll(".colour");

    function clearToolState() {
        canvas.isDrawingMode = false;
        canvas.selection = true;

        if (canvas.freeDrawingBrush) {
            canvas.freeDrawingBrush.color = currentColour;
            canvas.freeDrawingBrush.width = currentBrushSize;
        }
    }

    function setActiveTool(tool) {
        tools.forEach(button => {
            button.classList.remove("active");
        });

        tool.classList.add("active");
    }

    if (!viewOnly) {
        if (brushSizeControl) {
            brushSizeControl.addEventListener("pointerdown", event => {
                event.stopPropagation();
            });

            brushSizeControl.addEventListener("mousedown", event => {
                event.stopPropagation();
            });
        }

        if (brushSizeSlider) {
            brushSizeSlider.addEventListener("pointerdown", event => {
                event.stopPropagation();
            });

            brushSizeSlider.addEventListener("mousedown", event => {
                event.stopPropagation();
            });

            brushSizeSlider.addEventListener("click", event => {
                event.stopPropagation();
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

        tools.forEach(tool => {
            tool.addEventListener("click", () => {
                setActiveTool(tool);
                clearToolState();

                if (brushSizeControl) {
                    brushSizeControl.style.display =
                        tool.id === "pen" ? "flex" : "none";
                }

                if (tool.id === "pen") {
                    canvas.isDrawingMode = true;
                    canvas.selection = false;

                    if (!canvas.freeDrawingBrush) {
                        canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
                    }

                    canvas.freeDrawingBrush.color = currentColour;
                    canvas.freeDrawingBrush.width = currentBrushSize;
                }

                if (tool.id === "eraser") {
                    canvas.isDrawingMode = false;

                    const activeObjects = canvas.getActiveObjects();

                    activeObjects.forEach(object => {
                        canvas.remove(object);
                    });

                    canvas.discardActiveObject();
                    canvas.renderAll();
                }

                if (tool.id === "square") {
                    const rect = new fabric.Rect({
                        left: 100,
                        top: 100,
                        width: 100,
                        height: 100,
                        fill: "transparent",
                        stroke: currentColour,
                        strokeWidth: 3,
                        strokeUniform: true
                    });

                    canvas.add(rect);
                    canvas.setActiveObject(rect);
                }

                if (tool.id === "circle") {
                    const circle = new fabric.Circle({
                        left: 100,
                        top: 100,
                        radius: 50,
                        fill: "transparent",
                        stroke: currentColour,
                        strokeWidth: 3,
                        strokeUniform: true
                    });

                    canvas.add(circle);
                    canvas.setActiveObject(circle);
                }

                if (tool.id === "text") {
                    const text = new fabric.IText("Text", {
                        left: 100,
                        top: 100,
                        fill: currentColour,
                        fontSize: 24,
                        fontFamily: "Arial"
                    });

                    canvas.add(text);
                    canvas.setActiveObject(text);
                    text.enterEditing();
                }

                
                if (tool.id === "arrow") {
                    let startX = 0;
                    let startY = 0;
                    let isDrawingArrow = false;
                    let previewLine = null;
                    let previewHead = null;

                    const mouseDown = options => {
                        const pointer = canvas.getPointer(options.e);

                        startX = pointer.x;
                        startY = pointer.y;
                        isDrawingArrow = true;

                        previewLine = new fabric.Line(
                            [startX, startY, startX, startY],
                            {
                                stroke: currentColour,
                                strokeWidth: 3,
                                selectable: false,
                                evented: false
                            }
                        );

                        previewHead = new fabric.Polyline(
                            [
                                { x: startX, y: startY },
                                { x: startX, y: startY },
                                { x: startX, y: startY }
                            ],
                            {
                                fill: currentColour,
                                stroke: currentColour,
                                strokeWidth: 3,
                                selectable: false,
                                evented: false
                            }
                        );

                        canvas.add(previewLine, previewHead);
                    };

                    const mouseMove = options => {
                        if (!isDrawingArrow || !previewLine || !previewHead) {
                            return;
                        }

                        const pointer = canvas.getPointer(options.e);
                        const dx = pointer.x - startX;
                        const dy = pointer.y - startY;
                        const angle = Math.atan2(dy, dx);
                        const headLength = 12;

                        const x1 =
                            pointer.x - headLength * Math.cos(angle - Math.PI / 6);
                        const y1 =
                            pointer.y - headLength * Math.sin(angle - Math.PI / 6);

                        const x2 =
                            pointer.x - headLength * Math.cos(angle + Math.PI / 6);
                        const y2 =
                            pointer.y - headLength * Math.sin(angle + Math.PI / 6);

                        previewLine.set({
                            x1: startX,
                            y1: startY,
                            x2: pointer.x,
                            y2: pointer.y
                        });

                        previewHead.set({
                            points: [
                                { x: pointer.x, y: pointer.y },
                                { x: x1, y: y1 },
                                { x: x2, y: y2 }
                            ]
                        });

                        canvas.requestRenderAll();
                    };

                    const mouseUp = () => {
                        if (!isDrawingArrow) {
                            return;
                        }

                        isDrawingArrow = false;

                        if (previewLine && previewHead) {
                            const line = new fabric.Line(
                                [
                                    previewLine.x1,
                                    previewLine.y1,
                                    previewLine.x2,
                                    previewLine.y2
                                ],
                                {
                                    stroke: currentColour,
                                    strokeWidth: 3,
                                    strokeUniform: true
                                }
                            );

                            const arrowHead = new fabric.Polyline(
                                previewHead.points.map(point => ({
                                    x: point.x,
                                    y: point.y
                                })),
                                {
                                    fill: currentColour,
                                    stroke: currentColour,
                                    strokeWidth: 3,
                                    strokeLineJoin: "round",
                                    strokeUniform: true
                                }
                            );

                            canvas.remove(previewLine, previewHead);
                            canvas.add(line, arrowHead);
                            canvas.setActiveObject(
                                new fabric.ActiveSelection([line, arrowHead], { canvas })
                            );
                        }

                        previewLine = null;
                        previewHead = null;

                        canvas.off("mouse:down", mouseDown);
                        canvas.off("mouse:move", mouseMove);
                        canvas.off("mouse:up", mouseUp);

                        canvas.requestRenderAll();
                    };

                    canvas.on("mouse:down", mouseDown);
                    canvas.on("mouse:move", mouseMove);
                    canvas.on("mouse:up", mouseUp);
                }


                if (tool.id === "image") {
                    const imageLoader = document.getElementById("image-loader");

                    if (imageLoader) {
                        imageLoader.click();
                    }
                }
            });
        });

        colours.forEach(colour => {
            colour.addEventListener("click", () => {
                currentColour = colour.dataset.color;

                if (canvas.freeDrawingBrush) {
                    canvas.freeDrawingBrush.color = currentColour;
                }

                colours.forEach(button => {
                    button.classList.remove("active");
                });

                colour.classList.add("active");
            });
        });

        const imageLoader = document.getElementById("image-loader");

        if (imageLoader) {
            imageLoader.addEventListener("change", event => {
                const file = event.target.files[0];

                if (!file) {
                    return;
                }

                const reader = new FileReader();

                reader.onload = event => {
                    fabric.FabricImage.fromURL(event.target.result).then(image => {
                        image.scaleToWidth(250);

                        image.set({
                            left: 100,
                            top: 100
                        });

                        canvas.add(image);
                        canvas.setActiveObject(image);
                        canvas.renderAll();
                    });
                };

                reader.readAsDataURL(file);
                imageLoader.value = "";
            });
        }
    }

    if (typeof savedWhiteboard !== "undefined" && savedWhiteboard) {
        setTimeout(() => {
            try {
                canvas.loadFromJSON(savedWhiteboard).then(() => {
                    if (viewOnly) {
                        canvas.isDrawingMode = false;
                        canvas.selection = false;

                        canvas.forEachObject(object => {
                            object.selectable = false;
                            object.evented = false;
                        });

                        canvas.discardActiveObject();
                    }

                    canvas.renderAll();
                });
            } catch (error) {
                console.error("Failed to load whiteboard:", error);
            }
        }, 100);
    }

    if (!viewOnly) {
        let saveTimeout;

        function saveWhiteboard() {
            clearTimeout(saveTimeout);

            saveTimeout = setTimeout(() => {
                fetch(saveWhiteboardUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        whiteboard: JSON.stringify(canvas.toJSON())
                    })
                }).catch(error => {
                    console.error("Failed to save whiteboard:", error);
                });
            }, 500);
        }

        canvas.on("object:added", saveWhiteboard);
        canvas.on("object:modified", saveWhiteboard);
        canvas.on("object:removed", saveWhiteboard);
        canvas.on("path:created", saveWhiteboard);
    }

    window.addEventListener("resize", () => {
        canvas.setDimensions({
            width: whiteboardContainer.clientWidth,
            height: whiteboardContainer.clientHeight
        });

        canvas.renderAll();
    });
}