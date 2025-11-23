package com.uav.cursos_api;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/cursos")
public class CursoController {

    @Autowired
    private CursoRepository repositorio;

    @GetMapping
    public List<CursoModel> obtenerTodos() {
        return repositorio.findAll();
    }

    @PostMapping
    public CursoModel guardarCurso(@RequestBody CursoModel nuevoCurso) {
        return repositorio.save(nuevoCurso);
    }
}
