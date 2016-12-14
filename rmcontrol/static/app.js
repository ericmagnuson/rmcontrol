console.log('Starting app.');

new Vue({
    el: '#commands',
    data: {
        command: {
            name: ''
        },
        commands: []
    },
    mounted: function () {
        console.log('App ready.');
        this.fetchCommands();
    },
    methods: {
        fetchCommands: function () {
            this.$http.get('/commands').then(
                function(commands) {
                    console.log('Commands loaded.');
                    this.commands = commands.body;
                },
                function() {
                    console.log('There was an error retrieving commands.');
                }
            );
        },
        addCommand: function() {
            if (this.command.name) {
                this.$http.post('/commands', this.command).then(
                    function() {
                        this.commands.push(this.command);
                        this.command = {name: ''};
                    },
                    function() {
                        console.log('There was an error adding the command.');
                    }
                );
            }
        },
        fireCommand: function(command) {
            this.$http.post('/commands/' + command.name).then(
                function() {
                    console.log('Command fired.');
                },
                function() {
                    console.log('There was an error firing the command.');
                }
            );
        },
        editCommand: function(index) {

        },
        deleteCommand: function(index) {
            if (confirm("Are you sure you want to delete this command?")) {
                this.$http.delete('/commands/' + this.commands[index].name).then(
                    function() {
                        this.commands.splice(index, 1);
                    },
                    function() {
                        console.log('There was an error deleting the command.');
                    }
                );
            }
        }
    }
});
