<script setup>
import Header from '/src/components/Header.vue'
import Footer from '/src/components/Footer.vue'

</script>

<script>
export default {
    components: {
    },
    data() {
        return {
            alreadyReported: false,
            daysSince: 0,
            reports: [],
        }
    }, 
    computed: {
        warning_class() {
            if (this.daysSince < 2) {
                return "text-danger";
            }
            else if (this.daysSince < 8) {
                return "text-warning";
            }
            else {
                return "text-white";
            }
        },
    },
    methods: {
        format_report(raw_report) {
            var dateNow = Date(Date.now());
            var date = new Date(raw_report['infection_date']);
            // var date = data.setUTCSeconds(utcSeconds);
            if (raw_report['count'] == 1)
                var report = `Hubo ${raw_report['count']} caso el día ${date.toLocaleDateString()}`
            else
                var report = `Hubo ${raw_report['count']} casos el día ${date.toLocaleDateString()}`
            return report;
        },
        format_warning() {
            if (this.reports.length > 0) {
                var date = new Date(this.reports[0]['infection_date']);
                this.daysSince = Math.floor((Date.now() - date.valueOf()) / (1000 * 60 * 60 * 24));
                var warning = "";
                if (this.daysSince == 0) {
                    warning = "¡Ha habido un caso de piojos hoy!"
                }
                else if (this.daysSince == 1) {
                    warning = "¡Hubo un caso de piojos ayer!"
                }
                else if (this.daysSince < 7) {
                    warning = "Ha habido casos de piojos en la ultima semana!"
                }
                else {
                    warning = `No ha habido casos de piojos en los ultimos ${this.daysSince} dias`;
                }

                return warning;
            }
        },
        report() {
            this.$axios.post(import.meta.env.VITE_API_ENDPOINT + '/report_infection', {})
            .then(response => {
                this.alreadyReported = true;
                setTimeout(() => {this.alreadyReported = false}, 60000);

            })
            .catch(error => {
                console.error("error getting reports");
            });
        },
    },
    mounted() {
        this.$axios.post(import.meta.env.VITE_API_ENDPOINT + '/get_all_infections', {})
        .then(response => {
            this.reports = response.data;
        })
        .catch(error => {
            console.error("error getting reports");
        });
    }
}
</script>

<template>
    <div class="d-flex flex-column min-vh-100 text-white">
        <Header />
        <main role="main" class="main">
            <div class="container">
                <div class="row my-5 text-center border" style="min-height: 10em;"> 
                    <div class="col-12" :class="warning_class"> 
                        <h2 style="font-size: 5em">{{format_warning()}}</h2>
                    </div>
                </div>
                <div class="row"> 
                    <div class="offset-md-2 col-md-6 col-sm-12">
                    <button :disabled="alreadyReported" :class="alreadyReported? 'bg-light':'bg-secondary'" class="rounded-circle  border" @click="report">
                            <i v-if="alreadyReported"  class="fa-solid fa-face-smile fa-9x bd-placeholder-img rounded-circle bg-light text-primary bg-secondary" xmlns="http://www.w3.org/2000/svg" role="img" focusable="false"></i>
                            <i v-else class="fa-solid fa-bugs fa-9x bd-placeholder-img rounded-circle text-primary bg-secondary" xmlns="http://www.w3.org/2000/svg" role="img" focusable="false"></i>
                            <h1 v-if="!alreadyReported" class="text-white">¡He visto un piojo!</h1>
                            <h1 v-if="!alreadyReported" class="text-success">Clica aquí</h1>
                            <h1 v-else class="text-success">¡Gracias por avisar!</h1>
                        </button>   
                    </div>
                    <div class="col-md-3 col-sm-12">
                        <h2 class="mb-5">Registro de piojos</h2>
                        <div v-for="report in reports">
                            <h4>{{format_report(report)}}</h4>
                        </div>
                    </div>
                </div>
                
            </div>
        </main>
        <Footer class="mt-auto"/>
    </div>
</template>
