package com.pitchos.pitch.repository;

import com.pitchos.pitch.entity.Pitch;
import com.pitchos.pitch.entity.PitchStatus;
import com.pitchos.pitch.entity.PitchType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PitchRepository extends JpaRepository<Pitch, Long> {

    List<Pitch> findByPitchType(PitchType pitchType);

    List<Pitch> findByStatus(PitchStatus status);

    List<Pitch> findByPitchTypeAndStatus(PitchType pitchType, PitchStatus status);
}
