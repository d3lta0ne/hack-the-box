package com.hackthebox.breathtaking_view.Repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import com.hackthebox.breathtaking_view.Models.Users;
public interface UserRepository extends JpaRepository<Users, Long> {
    Users findByUsername(String username);
}
