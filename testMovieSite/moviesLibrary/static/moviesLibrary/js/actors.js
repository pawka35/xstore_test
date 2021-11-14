import {paginatorMixin} from "./paginatorMixin.js";

export const Actors =  {
    mixins: [paginatorMixin],
    data() {
        return {
            results: [],
       };
    },
    methods: {
        getData: function(){
            const path = `http://localhost:8000/api/actors/?page=${this.currentPage}`;
            console.log(path)

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
                    <th scope="col">Имя актера</th>
                    <th scope="col">Кол-во фильмов в которых снимался этот актер</th>
                    <th scope="col">Название жанра с лучшим средним рейтингом фильмов, в которых снимался актер</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(result, index) in results" :key="index">
                <td>{{ result.actor_name }}</td>
                <td>{{ result.movies_count }}</td>
                <td>{{ result.best_genre }}</td>
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
