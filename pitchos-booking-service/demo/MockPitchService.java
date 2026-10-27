import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.Map;

/**
 * PITCH SERVICE GIẢ LẬP (cổng 8082) — CHỈ DÙNG ĐỂ TẬP DEMO / KIỂM THỬ BOOKING SERVICE
 * khi Pitch Service thật của Linh chưa hoàn thiện. Dữ liệu giống pitchos-database/pitch-service.sql.
 *
 * Chạy:  java MockPitchService.java      (JDK 17+, không cần Maven)
 * Dừng:  Ctrl + C  (dùng để demo Booking Service trả 503)
 */
public class MockPitchService {

    private static final Map<Long, String> PITCHES = Map.of(
            1L, pitch(1, "Sân Bóng Đại Học Thể Thao (Sân 5)", "san_5", "300000.00", "Số 123 Đường Cầu Giấy, Quận Cầu Giấy, Hà Nội", "hoat_dong"),
            2L, pitch(2, "Sân Bóng Mỹ Đình Stadium (Sân 7)", "san_7", "500000.00", "Số 1 Lê Đức Thọ, Phường Mỹ Đình, Quận Nam Từ Liêm, Hà Nội", "hoat_dong"),
            3L, pitch(3, "Sân Vận Động Trung Tâm (Sân 10)", "san_10", "800000.00", "Khu Liên Hợp Thể Thao Tây Hồ, Hà Nội", "hoat_dong"),
            4L, pitch(4, "Sân Mini Phúc Diễn (Sân 5 - Đang sửa)", "san_5", "250000.00", "Phường Phúc Diễn, Quận Bắc Từ Liêm, Hà Nội", "bao_tri"));

    public static void main(String[] args) throws IOException {
        int port = args.length > 0 ? Integer.parseInt(args[0]) : 8082;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/api/v1/pitches/", MockPitchService::handle);
        server.start();
        System.out.println("Pitch Service GIẢ LẬP đang chạy tại http://localhost:" + port + "/api/v1/pitches/{id}");
    }

    private static void handle(HttpExchange ex) throws IOException {
        String path = ex.getRequestURI().getPath();
        System.out.println(ex.getRequestMethod() + " " + path);
        try {
            long id = Long.parseLong(path.substring("/api/v1/pitches/".length()));
            String body = PITCHES.get(id);
            if ("GET".equals(ex.getRequestMethod()) && body != null) {
                send(ex, 200, body);
                return;
            }
        } catch (NumberFormatException ignored) {
            // id không phải số → coi như không tồn tại
        }
        send(ex, 404, "{\"status\":404,\"error\":\"Not Found\",\"message\":\"Không tìm thấy sân bóng\"}");
    }

    private static void send(HttpExchange ex, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        ex.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = ex.getResponseBody()) {
            os.write(bytes);
        }
    }

    private static String pitch(long id, String name, String type, String price, String address, String status) {
        return String.format("{\"id\":%d,\"name\":\"%s\",\"pitchType\":\"%s\",\"pricePerHour\":%s,"
                + "\"address\":\"%s\",\"status\":\"%s\"}", id, name, type, price, address, status);
    }
}
