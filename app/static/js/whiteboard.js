const whiteboardElement = document.getElementById("whiteboard");

if (whiteboardElement) {
    let currentColour = "#1F2937";

    const canvas = new fabric.Canvas("whiteboard");

    // Canvas setup
    canvas.setDimensions({
        width: 1070,
        height: 500
    });

    // Pen setup
    canvas.isDrawingMode = false;

    canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
    canvas.freeDrawingBrush.width = 3;
    canvas.freeDrawingBrush.color = currentColour;

    // Custom tool states tracker
    let isArrowModeActive = false;
    let isDrawingArrow = false;
    let line;
    let arrowhead;

    // Reset state when switching tools
    function clearToolState() {
        isArrowModeActive = false;
        isDrawingArrow = false;
        line = null;
        arrowhead = null;
        
        // Restore standard canvas behaviors
        canvas.isDrawingMode = false;
        canvas.selection = true; 
        canvas.defaultCursor = 'default';
    }

    // Show toggle between tools
    const tools = document.querySelectorAll(".tool");

    tools.forEach(tool => {
        tool.addEventListener("click", () => {
            // Remove active from all tools
            tools.forEach(t => t.classList.remove("active"));

            // Activate clicked tool
            tool.classList.add("active");
            
            clearToolState();
        });
    });

    // Show toggle between colours
    const colourButtons = document.querySelectorAll(".colour");

    colourButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Remove tick from all colours
            colourButtons.forEach(btn => {
                btn.classList.remove("active");
            });

            // Add tick to selected colour
            button.classList.add("active");

            // Change drawing colour
            currentColour = button.dataset.color;
            if (canvas.freeDrawingBrush) {
                canvas.freeDrawingBrush.color = currentColour;
            }
        });
    });

    // Pen functionality
    const penButton = document.getElementById("pen");

    if (penButton) {
        penButton.addEventListener("click", () => {
            // clearCustomTools runs right before this via the .tool click event listener
            canvas.isDrawingMode = true;
            canvas.freeDrawingBrush.color = currentColour; // Fixed to use active currentColour
            canvas.freeDrawingBrush.width = 3;
        });
    }

    // Eraser functionality
    const eraserButton = document.getElementById("eraser");

    if (eraserButton) {
        eraserButton.addEventListener("click", () => {
            const activeObject = canvas.getActiveObject();

            if (activeObject) {
                canvas.remove(activeObject);
                canvas.discardActiveObject();
                canvas.requestRenderAll();
            }
        });
    }

    // Square functionality
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

    // Circle functionality
    const circleButton = document.getElementById("circle");

    if (circleButton) {
        circleButton.addEventListener("click", () => {
            const circle = new fabric.Ellipse({
                left: 100,
                top: 100,
                rx: 50, // Fixed: rx and ry should be half of the target diameter (50 = 100px total width)
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

    // Text functionality
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

    // Arrow functionality
    const arrowButton = document.getElementById("arrow");

    if (arrowButton) {
        arrowButton.addEventListener("click", () => {
            // clearCustomTools runs right before this via the .tool click event listener
            isArrowModeActive = true;
            canvas.selection = false;
            canvas.defaultCursor = 'crosshair';
        });
    }

    // Create line and arrowhead on click
    canvas.on('mouse:down', function (options) {
        if (!isArrowModeActive || options.target) return;

        isDrawingArrow = true;
        const pointer = canvas.getPointer(options.e);
        const color = currentColour;
        
        // Create the line
        line = new fabric.Line([pointer.x, pointer.y, pointer.x, pointer.y], {
            strokeWidth: 3,
            stroke: color,
            fill: 'transparent',
            originX: 'center',
            originY: 'center',
            selectable: false,
            hoverCursor: 'default'
        });

        // Create the triangle point
        arrowhead = new fabric.Triangle({
            width: 15,
            height: 15,
            fill: color,
            left: pointer.x,
            top: pointer.y,
            originX: 'center',
            originY: 'center',
            selectable: false,
            angle: 0,
            hoverCursor: 'default'
        });

        canvas.add(line, arrowhead);
    });

    // Update line with math as mouse moves
    canvas.on('mouse:move', function (options) {
        if (!isDrawingArrow || !line || !arrowhead) return;

        const pointer = canvas.getPointer(options.e);

        line.set({ x2: pointer.x, y2: pointer.y });

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

    canvas.on('mouse:up', function () {
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

    // Image functionality
    const imageToolBtn = document.getElementById('image');
    const imageLoader = document.getElementById('image-loader');

    // Open image upload
    imageToolBtn.addEventListener('click', () => {
        imageLoader.click();
    });

    // Listen for file selection
    imageLoader.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        
        // Convert selected local file into secure DataURL string
        reader.onload = function(event) {
            const imgDataUrl = event.target.result;

            // Use Fabric v6 syntax to load the image onto the canvas grid
            fabric.Image.fromURL(imgDataUrl).then((fabricImg) => {
                
                const maxDimension = Math.min(canvas.width, canvas.height) * 0.6;
                if (fabricImg.width > maxDimension || fabricImg.height > maxDimension) {
                    fabricImg.scaleToWidth(maxDimension);
                }

                // Centre the uploaded asset within your existing boundary box
                fabricImg.set({
                    left: canvas.width / 2 - (fabricImg.getScaledWidth() / 2),
                    top: canvas.height / 2 - (fabricImg.getScaledHeight() / 2),
                    cornerColor: '#3B82F6',
                    cornerStrokeColor: '#1E40AF',
                    transparentCorners: false,
                    cornerSize: 10
                });

                // Commit object straight to the scene context and refresh the view layer
                canvas.add(fabricImg);
                canvas.setActiveObject(fabricImg);
                canvas.requestRenderAll();
            });
        };

        reader.readAsDataURL(file);
        
        // Clear input value so the same image can be re-uploaded back-to-back if needed
        this.value = '';
    });

}
