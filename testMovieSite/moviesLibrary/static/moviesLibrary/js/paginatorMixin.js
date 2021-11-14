export var paginatorMixin = {
    data() {
        return {
            results: [],
            currentPage:1,
            showNextButton: false,
            showBackButton: false,
        };
    },
    methods: {
        loadNext() {
            this.currentPage += 1;
            this.getData();
        },
        loadPrev() {
            this.currentPage -= 1;
            this.getData();
        },
    },
};
