const whiteboardElement = document.getElementById("whiteboard");

if (whiteboardElement) {
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
    canvas.freeDrawingBrush.color = "#000000";

    // Pen functionality
    const penButton = document.getElementById("pen");

    if (penButton) {
        penButton.addEventListener("click", () => {
            canvas.isDrawingMode = true;
            canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
            canvas.freeDrawingBrush.width = 3;
            canvas.freeDrawingBrush.color = "#000000";
        });
    }

    // Eraser functionality
    const eraserButton = document.getElementById("eraser");

    if (eraserButton) {
        eraserButton.addEventListener("click", () => {
            canvas.isDrawingMode = false;

            const activeObject = canvas.getActiveObject();

            if (activeObject) {
                canvas.remove(activeObject);
                canvas.discardActiveObject();
                canvas.requestRenderAll();
            }
        });
    }

    // Shape functionality
    const shapeButton = document.getElementById("shape");

    if (shapeButton) {
        shapeButton.addEventListener("click", () => {
            canvas.isDrawingMode = false;

            const rectangle = new fabric.Rect({
                left: 100,
                top: 100,
                width: 100,
                height: 100,
                fill: "transparent",
                stroke: "black",
                strokeWidth: 2
            });

            canvas.add(rectangle);
            canvas.setActiveObject(rectangle);
        });
    }

    // Text functionality
    const textButton = document.getElementById("text");

    if (textButton) {
        textButton.addEventListener("click", () => {
            canvas.isDrawingMode = false;

            const text = new fabric.IText("Text", {
                left: 100,
                top: 100,
                fontSize: 20,
                fill: "#000000",
                fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"'
            });

            canvas.add(text);
            canvas.setActiveObject(text);
            text.enterEditing();
        });
    }
}