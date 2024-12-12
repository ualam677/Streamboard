<script>
import axios from 'axios';

export default {
    data() {
        return {
            message: ''
        };
    },
    mounted() {
        axios.get('http://127.0.0.1:8000/api/test/')
            .then(response => {
                this.message = response.data.message;
            });
    }
};
</script>