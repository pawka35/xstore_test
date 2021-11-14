import {paginatorMixin} from "./paginatorMixin.js";
export const Directors =  {
    mixins: [paginatorMixin],
    data() {
        return {
            results: [],
       };
    },
    methods: {
        getData: function(){
            const path = `http://localhost:8000/api/directors/?page=${this.currentPage}`;
            fetch(path)
            .then(res=> res.json())
            .then((res)=> {
                this.results = res.results
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
                    <th scope="col">Режиссер</th>
                    <th scope="col">Актеры, чаще всего снималившиеся с этим режиссером в
                    порядке убывания количества фильмов и само количество фильмов. До первых трёх записей</th>
                    <th scope="col">3 лучших фильма режиссера по рейтингу.</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(result, index) in results" :key="index">
                <td>{{ result.director_name }}</td>
                <td>
                    <tr v-for="favourite_actor in result.favourite_actors" :key="favourite_actor.name">
                        <td class="mt-13"> Актер: {{ favourite_actor.name }} </td>
                        <td> Кол-во фильмов: {{ favourite_actor.movie_count }} </td>
                    </tr>
                </td>
                <td>
                    <tr v-for="best_movie in result.best_movies">
                        <td>{{ best_movie }}</td>
                    </tr>
                </td>
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
