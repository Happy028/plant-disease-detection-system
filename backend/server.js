const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Setup file storage with multer
const upload = multer({ dest: "uploads/" });

// POST endpoint to handle image uploads and run model inference
app.post("/predict", upload.single("file"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    const imagePath = path.join(__dirname, req.file.path);
    
    // Call the Python script for inference
    const pythonProcess = spawn("python3", ["model/model.py", imagePath]);

    pythonProcess.stdout.on("data", (data) => {
        const prediction = data.toString().trim();
        res.json({ prediction });  // Send prediction as JSON response
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Error: ${data}`);
        res.status(500).json({ error: "Model inference failed" });
    });

    pythonProcess.on("close", () => {
        // Cleanup the uploaded file after prediction
        fs.unlinkSync(imagePath);
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
