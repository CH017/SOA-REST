package com.uav.cursos_api;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class CursoService {

    @Autowired
    private CursoRepository cursoRepository;

    public List<CursoModel> obtenerCursos() {
        return cursoRepository.findAll();
    }

    public Optional<CursoModel> obtenerCursoPorId(Integer id) {
        return cursoRepository.findById(id);
    }

    public CursoModel guardarCurso(CursoModel curso) {
        return cursoRepository.save(curso);
    }

    public void eliminarCurso(Integer id) {
        cursoRepository.deleteById(id);
    }
}
