package com.pitchos.auth.service;

import com.pitchos.auth.dto.LoginRequest;
import com.pitchos.auth.dto.LoginResponse;
import com.pitchos.auth.dto.RegisterRequest;
import com.pitchos.auth.dto.UserResponse;
import com.pitchos.auth.entity.Role;
import com.pitchos.auth.entity.User;
import com.pitchos.auth.exception.BadRequestException;
import com.pitchos.auth.exception.ResourceNotFoundException;
import com.pitchos.auth.exception.UnauthorizedException;
import com.pitchos.auth.repository.UserRepository;
import com.pitchos.auth.security.JwtTokenProvider;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class AuthService {

    private static final Logger log = LoggerFactory.getLogger(AuthService.class);

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    public AuthService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder,
                       JwtTokenProvider jwtTokenProvider) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    /**
     * Đăng ký tài khoản mới. Mật khẩu được băm BCrypt trước khi lưu xuống CSDL,
     * vai trò luôn cố định là 'user' — client không được phép tự chọn role.
     */
    @Transactional
    public UserResponse register(RegisterRequest request) {
        log.info("Đăng ký tài khoản mới: {}", request.getUsername());

        String username = request.getUsername().trim();
        String email = request.getEmail().trim();

        if (userRepository.existsByUsername(username)) {
            throw new BadRequestException("Tên đăng nhập '" + username + "' đã tồn tại trong hệ thống");
        }
        if (userRepository.existsByEmail(email)) {
            throw new BadRequestException("Email '" + email + "' đã được sử dụng cho tài khoản khác");
        }

        User user = User.builder()
                .username(username)
                .email(email)
                // Băm một chiều bằng BCrypt: CSDL không bao giờ lưu mật khẩu dạng văn bản thuần
                .password(passwordEncoder.encode(request.getPassword()))
                .fullName(request.getFullName().trim())
                .phone(request.getPhone() != null && !request.getPhone().isBlank()
                        ? request.getPhone().trim() : null)
                .role(Role.user)
                .build();

        User saved = userRepository.save(user);
        log.info("Đã tạo tài khoản ID {} với vai trò mặc định '{}'", saved.getId(), saved.getRole());
        return UserResponse.fromEntity(saved);
    }

    /**
     * Đăng nhập: so khớp mật khẩu với bản băm BCrypt rồi cấp phát Bearer JWT Token.
     * Cố ý trả về cùng một thông báo cho cả trường hợp sai tên đăng nhập và sai mật khẩu,
     * để không tiết lộ tài khoản nào đang tồn tại trong hệ thống.
     */
    @Transactional(readOnly = true)
    public LoginResponse login(LoginRequest request) {
        log.info("Yêu cầu đăng nhập của tài khoản: {}", request.getUsername());

        User user = userRepository.findByUsername(request.getUsername().trim())
                .orElseThrow(() -> new UnauthorizedException("Tên đăng nhập hoặc mật khẩu không đúng"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            log.warn("Đăng nhập thất bại: sai mật khẩu cho tài khoản '{}'", user.getUsername());
            throw new UnauthorizedException("Tên đăng nhập hoặc mật khẩu không đúng");
        }

        String accessToken = jwtTokenProvider.generateToken(user);

        return LoginResponse.builder()
                .accessToken(accessToken)
                .tokenType("Bearer")
                .expiresIn(jwtTokenProvider.getExpiresInSeconds())
                .userId(user.getId())
                .username(user.getUsername())
                .fullName(user.getFullName())
                .role(user.getRole())
                .build();
    }

    /**
     * Tra cứu người dùng theo ID, kèm kiểm tra quyền sở hữu tài nguyên:
     * tài khoản 'user' chỉ được xem thông tin của chính mình, cố xem người khác sẽ nhận 403 Forbidden.
     * 'chusan' và 'admin' được xem mọi tài khoản.
     */
    @Transactional(readOnly = true)
    public UserResponse getUserById(Long id, String currentUsername) {
        User target = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Không tìm thấy người dùng với mã ID: " + id));

        User current = userRepository.findByUsername(currentUsername)
                .orElseThrow(() -> new UnauthorizedException("Phiên đăng nhập không hợp lệ"));

        if (current.getRole() == Role.user && !current.getId().equals(target.getId())) {
            log.warn("Từ chối truy cập: '{}' (role user) cố xem thông tin của user ID {}",
                    currentUsername, id);
            throw new AccessDeniedException(
                    "Truy cập bị từ chối. Tài khoản vai trò 'user' chỉ được xem thông tin của chính mình.");
        }

        return UserResponse.fromEntity(target);
    }

    /**
     * Lấy thông tin tài khoản đang đăng nhập dựa trên username trong JWT.
     */
    @Transactional(readOnly = true)
    public UserResponse getCurrentUser(String currentUsername) {
        User user = userRepository.findByUsername(currentUsername)
                .orElseThrow(() -> new UnauthorizedException("Phiên đăng nhập không hợp lệ"));
        return UserResponse.fromEntity(user);
    }

    /**
     * Danh sách toàn bộ người dùng — chỉ dành cho vai trò 'admin'.
     */
    @Transactional(readOnly = true)
    public List<UserResponse> getAllUsers() {
        return userRepository.findAll().stream()
                .map(UserResponse::fromEntity)
                .toList();
    }
}
