class CourseController {
    findAll(req, res) {
        res.send("Todos os cursos");
    }

    create(req, res) {
        res.send("Curso criado");
    }

    delete(req, res) {
        res.send("Curso deletado");
    }

    edit(req, res) {
        res.send("Curso editado");
    }
}

export default new CourseController();