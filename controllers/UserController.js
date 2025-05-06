class UserController {
    create(req, res) {
        res.send("Cria usuário");
    }

    login(req, res) {
        res.send("Login usuário");
    }
}

export default new UserController();