const API_URL = "http://localhost:8000";

export async function uploadVideo(file: File){
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
    });

    console.log('Response status:', response.status);

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to upload video");
    }

    return await response.json();
}