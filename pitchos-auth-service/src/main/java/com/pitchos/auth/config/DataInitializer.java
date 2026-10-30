package com.pitchos.auth.config;

import com.pitchos.auth.entity.Role;
import com.pitchos.auth.entity.User;
import com.pitchos.auth.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * Khởi tạo 3 tài khoản mẫu đại diện cho 3 vai trò, phục vụ kiểm thử và demo hội đồng.
 *
 * Lớp này cũng tự kiểm tra lại mật khẩu của 3 tài khoản mẫu: chuỗi băm BCrypt được nạp
 * sẵn trong file auth-user-service.sql có thể không khớp với mật khẩu '123456' ghi trong
 * chú thích (đó là chuỗi băm mẫu lấy từ tài liệu Spring Security). Nếu phát hiện lệch,
 * hệ thống sẽ băm lại bằng BCryptPasswordEncoder và ghi log cảnh báo, tránh tình huống
 * đăng nhập thất bại ngay bước đầu khi demo.
 */
@Component
public class DataInitializer implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DataInitializer.class);

    /** Mật khẩu mặc định của 3 tài khoản mẫu, khớp chú thích trong auth-user-service.sql */
    private static final String DEFAULT_PASSWORD = "123456";

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    @Transactional
    public void run(String... args) {
        if (userRepository.count() == 0) {
            log.info("CSDL chưa có tài khoản nào. Đang khởi tạo 3 tài khoản mẫu cho 3 vai trò...");

            List<User> initialUsers = List.of(
                    User.builder()
                            .username("admin")
                            .email("admin@gmail.com")
                            .password(passwordEncoder.encode(DEFAULT_PASSWORD))
                            .fullName("Quản Trị Viên Hệ Thống")
                            .phone("0901112222")
                            .role(Role.admin)
                            .build(),
                    User.builder()
                            .username("chusan")
                            .email("chusan@gmail.com")
                            .password(passwordEncoder.encode(DEFAULT_PASSWORD))
                            .fullName("Trần Văn Chủ Sân")
                            .phone("0987654321")
                            .role(Role.chusan)
                            .build(),
                    User.builder()
                            .username("user")
                            .email("user@gmail.com")
                            .password(passwordEncoder.encode(DEFAULT_PASSWORD))
                            .fullName("Nguyễn Văn Khách Hàng")
                            .phone("0912345678")
                            .role(Role.user)
                            .build()
            );

            userRepository.saveAll(initialUsers);
            log.info("Khởi tạo thành công {} tài khoản mẫu (mật khẩu dùng chung: {})",
                    initialUsers.size(), DEFAULT_PASSWORD);
        } else {
            log.info("CSDL đã có sẵn {} tài khoản người dùng.", userRepository.count());
            repairDemoPasswords();
        }
    }

    /**
     * Soát lại 3 tài khoản mẫu: nếu chuỗi băm hiện tại không khớp mật khẩu mặc định
     * thì băm lại cho đúng, để kịch bản demo luôn đăng nhập được.
     */
    private void repairDemoPasswords() {
        for (String username : List.of("admin", "chusan", "user")) {
            Optional<User> found = userRepository.findByUsername(username);
            if (found.isEmpty()) {
                continue;
            }

            User user = found.get();
            if (!passwordEncoder.matches(DEFAULT_PASSWORD, user.getPassword())) {
                log.warn("Tài khoản '{}' có chuỗi băm BCrypt không khớp mật khẩu mặc định '{}'. "
                        + "Đang băm lại để phục vụ kiểm thử và demo.", username, DEFAULT_PASSWORD);
                user.setPassword(passwordEncoder.encode(DEFAULT_PASSWORD));
                userRepository.save(user);
            }
        }
    }
}
