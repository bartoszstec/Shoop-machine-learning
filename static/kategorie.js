const { createApp } = Vue

const CategoryApp = {
    data(){
        return {
            kategorie: [
                {nazwa:"AGD", url:"/kategorie/AGD"},
                {nazwa:"RTV", url:"/kategorie/RTV"},
                {nazwa:"Telefony", url:"/kategorie/Telefony"},
                {nazwa:"Odzież", url:"/kategorie/Odzież"},
                {nazwa:"Sport", url:"/kategorie/Sport"},
                {nazwa:"Zegarki i biżuteria", url:"/kategorie/Zegarki%20i%20bi%C5%BCuteria"} // Użyj kodowania URL dla spacji i specjalnych znaków
            ],
            isHovered: [false, false, false, false, false, false] // Zmienna śledząca stan najechania na każdy kafelek
        }
    },
    methods: {
        hoverCategory(index) {
            this.isHovered[index] = true; // Ustawienie true dla najechanego kafelka
        },
        leaveCategory(index) {
            this.isHovered[index] = false; // Ustawienie false dla opuszczonego kafelka
        }
    },
    delimiters: ['{','}']
}

createApp(CategoryApp).mount('#kategorie')