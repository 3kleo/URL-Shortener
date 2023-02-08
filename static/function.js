function showNotification(){
    console.log("here");
    var visible = document.getElementById("copy_notification");
    var copiedMsg = document.querySelector("#copy_notification h4");
    copiedMsg.innerHTML = "Link copied!"
    visible.classList.remove("hidden")
    visible.classList.add("visible")
    setTimeout(() => {
      visible.classList.remove("visible")
      visible.classList.add("hidden")
      copiedMsg.innerHTML = ""
      }, 1000)
  }

async function copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      // console.log('Text copied to clipboard');
    } catch (err) {
      // console.error('Failed to copy text: ', err);
    }
  }
