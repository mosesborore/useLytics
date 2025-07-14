
function showToast(message, messageLevel) {
    const toast = document.createElement("div");
    toast.className = `alert alert-${messageLevel}`;
    toast.innerText = message;

    toast.addEventListener("click", () => {
        toast.remove();
    });

    document.getElementById("toast-container").appendChild(toast);

    setTimeout(() => {
        if (toast.parentNode) toast.remove();
    }, 5000); // Auto-dismiss after 5 seconds
}