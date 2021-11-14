import {paginatorMixin} from "./paginatorMixin.js";
export const Genres =  {
    mixins: [paginatorMixin],
    data() {
        return {
            genres: [],
       };
    },
    methods: {
        getData() {
            const path = `http://localhost:8000/api/genres/?page=${this.currentPage}`;
            fetch(path)
            .then(res=> res.json())
            .then((res)=> {
                this.genres = res.results;
                this.showNextButton = false;
                this.showBackButton = false;
                if (res.next) {
                    this.showNextButton = true;
                };
                if (res.previous) {
                    this.showBackButton = true;
                };
            });
        },
    },
    created() {
        this.getData();
    },
    template: `
    <div>
        <table class="table table-hover">
            <thead>
                <tr>
                    <th scope="col">Название жанра</th>
                    <th scope="col">Кол-во фильмов этого жанра</th>
                    <th scope="col">Средняя оценка фильмов данного жанра</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(genre, index) in genres" :key="index">
                <td>{{ genre.genre }}</td>
                <td>{{ genre.movie_count }}</td>
                <td>{{ genre.avg_rating }}</td>
                </tr>
            </tbody>
        </table>
        <div class="row">
            <div v-if="showBackButton" class="col">
                <button class="btn btn-outline-primary" @click="loadPrev()">Back</button>
            </div>
            <div v-if="showNextButton" class="col">
                <button class="btn btn-outline-primary" @click="loadNext()">Next</button>
            </div>
        </div>
    </div>
`
};
