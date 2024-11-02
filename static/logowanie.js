const { createApp } = Vue

const LoginApp = {
    data() {
        return {
            isLogin: true, // Domyślnie pokazuje formularz logowania
            changePasswordType: 'password'
        }
    },
    methods: {
        toggleForm() {
            this.isLogin = !this.isLogin;
        },
        togglePasswordVisibility() {
            this.changePasswordType = this.changePasswordType === 'password' ? 'text' : 'password';
        },
    },
    delimiters: ['{','}']
}

createApp(LoginApp).mount('#logowanie')