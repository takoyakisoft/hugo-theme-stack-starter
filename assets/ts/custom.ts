document.addEventListener('DOMContentLoaded', (): void => {  
  function setBodyClass(): void {  
    const isDark: boolean = document.documentElement.dataset.scheme === "dark";  
  
    if (isDark) {  
      document.body.classList.add("dark");  
    } else {  
      document.body.classList.remove("dark");  
    }  
  }  
  
  setBodyClass();  
  
  window.addEventListener("onColorSchemeChange", (e: CustomEvent): void => {  
    setBodyClass();  
  });  
});