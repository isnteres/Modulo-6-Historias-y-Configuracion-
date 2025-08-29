document.addEventListener("DOMContentLoaded", () => {
    const menuLinks = document.querySelectorAll(".menu a");
    const sections = document.querySelectorAll(".section");

    menuLinks.forEach(link => {
        link.addEventListener("click", e => {
            e.preventDefault();
            menuLinks.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            const sectionId = link.getAttribute("data-section");
            sections.forEach(sec => sec.style.display = "none");

            const target = document.getElementById(sectionId);
            target.style.display = "block";

            if (sectionId === "historias") {
                cargarHistorias();
            } else if (sectionId === "configuraciones") {
                cargarConfiguraciones();
            }
        });
    });

    // Inicialmente carga historias
    cargarHistorias();
});
