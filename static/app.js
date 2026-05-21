const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const fileInfo = document.getElementById("fileInfo");
const dropContent = document.querySelector(".drop-content");
const fileName = document.getElementById("fileName");
const fileSize = document.getElementById("fileSize");
const removeFileBtn = document.getElementById("removeFile");
const submitBtn = document.getElementById("submitBtn");
const form = document.getElementById("uploadForm");
const progressContainer = document.getElementById("progressContainer");
const progressBar = document.getElementById("progressBar");
const percentage = document.getElementById("percentage");
const statusText = document.getElementById("statusText");

// Drag and Drop Events
dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");

    if (e.dataTransfer.files.length) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
        handleFile(fileInput.files[0]);
    }
});

function handleFile(file) {
    if (!file.name.endsWith(".srt")) {
        alert("لطفاً فقط فایل .srt آپلود کنید.");
        return;
    }

    // Update File Info
    fileName.innerText = file.name;
    fileSize.innerText = formatBytes(file.size);

    // UI Updates
    dropContent.style.display = "none";
    fileInfo.style.display = "flex";
    submitBtn.disabled = false;

    // Manually set input files if coming from drag/drop
    if (fileInput.files[0] !== file) {
        const dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;
    }
}

removeFileBtn.addEventListener("click", (e) => {
    e.stopPropagation(); // prevent triggering dropZone click
    resetFile();
});

function resetFile() {
    fileInput.value = "";
    dropContent.style.display = "block";
    fileInfo.style.display = "none";
    submitBtn.disabled = true;
    progressContainer.classList.remove("active");
    progressBar.style.width = "0%";
    percentage.innerText = "0%";
}

function formatBytes(bytes, decimals = 2) {
    if (!+bytes) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}

// Form Submission
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!fileInput.files.length) return;

    // UI Reset for Translation Start
    submitBtn.disabled = true;
    submitBtn.classList.add("loading");
    progressContainer.classList.remove("active");

    // Wait a tick then show progress
    setTimeout(() => {
        progressContainer.classList.add("active");
        statusText.innerText = "در حال ترجمه...";
    }, 100);

    const formData = new FormData(form);

    // Initial width
    progressBar.style.width = "0%";

    // Start Polling Progress
    let pollInterval = setInterval(async () => {
        try {
            const res = await fetch("/progress");
            const data = await res.json();
            const val = data.value;
            progressBar.style.width = val + "%";
            percentage.innerText = val + "%";

            if (val >= 100) statusText.innerText = "در حال نهایی سازی...";
        } catch (err) {
            console.error("Progress poll error", err);
        }
    }, 500);

    try {
        const response = await fetch("/translate", {
            method: "POST",
            body: formData
        });

        clearInterval(pollInterval);

        if (response.ok) {
            progressBar.style.width = "100%";
            percentage.innerText = "100%";
            statusText.innerText = "✅ ترجمه کامل شد";

            // Download File
            const blob = await response.blob();
            const originalName = fileInput.files[0].name;
            const downloadName = "translated_" + originalName;

            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = downloadName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            // Reset button state
            submitBtn.classList.remove("loading");
            submitBtn.disabled = false;
        } else {
            throw new Error("Translation failed");
        }
    } catch (error) {
        clearInterval(pollInterval);
        statusText.innerText = "❌ خطا در ترجمه";
        statusText.style.color = "#ef4444";
        submitBtn.classList.remove("loading");
        submitBtn.disabled = false;
    }
});
