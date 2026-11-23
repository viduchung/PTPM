# Kịch bản thuyết trình — Slide kiến trúc tổng thể PitchOS

Dùng cho tệp `E:\SLIDE_KIEN_TRUC_PitchOS.pptx` (9 slide). Người trình bày: Lê Đức Hoàng, Nhóm 13.

Phần in **"trong ngoặc kép"** là lời nói — đọc được nguyên văn. Phần **Chỉ vào** là động tác. Phần **Lưu ý** không đọc.

Lời nói đã được viết vừa đúng thời lượng từng slide ở tốc độ **khoảng 150 từ mỗi phút** — tốc độ nói rõ ràng, có chỗ ngắt. Đọc nhanh hơn sẽ thừa thời gian, đọc chậm hơn sẽ vỡ giờ. Nên đọc to đúng một lượt trước khi lên, bấm đồng hồ.

---

## A. Trước khi vào phòng

**Kiểm tra trong 5 phút:**

1. Docker Desktop đã bật, container `pitchos-mysql` đang chạy
2. Ba dịch vụ đã lên: mở `http://localhost:8081/swagger-ui.html`, `:8082`, `:8083` — cả ba ra trang Swagger
3. Postman đã mở sẵn ba collection, đã chạy thử một lượt
4. Slide mở ở chế độ Presenter View để thấy ghi chú thời lượng
5. Tắt thông báo Windows, tắt Zalo và Messenger

**Nếu máy có sự cố:** cứ trình bày slide bình thường, nói thẳng *"phần demo trực tiếp em xin trình bày sau, hiện máy đang có sự cố"*. Slide tự đứng được, không cần hệ thống chạy.

**Bảng thời gian:**

| Slide | Nội dung | Giây | Mốc tích lũy |
|---|---|---|---|
| 1 | Bìa | 40 | 0:40 |
| 2 | Bài toán và ý tưởng | 50 | 1:30 |
| 3 | Phạm vi chức năng | 45 | 2:15 |
| 4 | **Kiến trúc tổng thể** | 65 | 3:20 |
| 5 | Phân chia trách nhiệm | 55 | 4:15 |
| 6 | **Luồng đặt sân 450.000đ** | 90 | 5:45 |
| 7 | **Xử lý lỗi và nhất quán** | 70 | 6:55 |
| 8 | Kết quả và giới hạn | 50 | 7:45 |
| 9 | Hướng phát triển | 50 | **8:35** |

Ba slide in đậm là phần trọng tâm — nếu bị nhắc nhanh lên, cắt bớt slide 3 và 9, **không cắt** slide 4, 6, 7.

---

## B. Kịch bản từng slide

### Slide 1 — Bìa · 40 giây

**Chỉ vào:** không chỉ gì, đứng thẳng, nhìn thầy.

> "Thưa thầy, em là Lê Đức Hoàng, đại diện Nhóm 13. Đề tài của nhóm em là hệ thống quản lý đặt sân bóng đá, xây dựng theo kiến trúc microservices và giao tiếp bằng REST.
>
> Phần trình bày hôm nay gồm ba câu hỏi chính: vì sao nhóm em chia hệ thống thành ba dịch vụ, ba dịch vụ đó nói chuyện với nhau ra sao, và một yêu cầu đặt sân của khách đi qua những bước nào bên trong hệ thống.
>
> Nhóm em có bốn người: em, bạn Hùng, bạn Linh và bạn Nhật."

**Câu chuyển:** "Em xin bắt đầu từ bài toán."

**Lưu ý:** Nói chậm ở ba câu hỏi — đó là lời hứa về cấu trúc bài nói, thầy sẽ theo đó mà nghe.

---

### Slide 2 — Bài toán và ý tưởng · 50 giây

**Chỉ vào:** ô "Khách hàng" bên trái → bốn thẻ số ở giữa → khung câu hỏi màu xanh dưới cùng.

> "Giả sử một khách muốn đặt sân A từ chín giờ đến mười giờ ba mươi. Với khách, đó chỉ là một lần bấm nút.
>
> Nhưng bên trong, hệ thống phải làm bốn việc. Một là xác thực danh tính. Hai là tra đơn giá sân, vì tiền phải do hệ thống tính chứ không để khách tự khai. Ba là kiểm tra khung giờ đã có ai giữ chưa. Bốn là tính tiền và ghi đơn.
>
> Bốn bước này phải xong hết trước khi trả lời khách. Và câu hỏi khó nhất của cả đề tài là câu dưới đây: nếu hai khách bấm đặt cùng một khung giờ trong cùng một giây, ai được sân?"

**Câu chuyển:** "Em xin trả lời câu này ở slide thứ bảy. Trước đó, xin nói về phạm vi."

**Lưu ý:** Dừng một nhịp sau câu hỏi, đừng trả lời ngay. Đó là điểm neo của cả bài — slide 7 sẽ trả lời và thầy nhớ ra mình từng đặt câu hỏi đó.

---

### Slide 3 — Phạm vi chức năng · 45 giây

**Chỉ vào:** ba thẻ lần lượt từ trái sang phải → khung "Ngoài phạm vi" ở dưới.

> "Hệ thống gồm ba nhóm chức năng. Thứ nhất là tài khoản và phân quyền: đăng ký, đăng nhập, cấp token, với ba vai trò khách, chủ sân và quản trị. Thứ hai là danh mục sân: danh sách sân, đơn giá mỗi giờ, và chuyển sân sang bảo trì. Thứ ba là đặt sân và duyệt đơn, trong đó có phần chống đặt trùng khung giờ.
>
> Hai việc nhóm em chủ động để ngoài phạm vi. Một là thanh toán: khách trả tiền trực tiếp tại sân, nên đơn đặt không có trạng thái đã trả tiền. Hai là giao diện web — hiện nhóm em demo qua Swagger và Postman."

**Câu chuyển:** "Bây giờ xin đi vào kiến trúc."

**Lưu ý:** Nói "chủ động để ngoài phạm vi", không nói "chưa làm được". Hai cách nói cho hai ấn tượng rất khác.

---

### Slide 4 — Kiến trúc tổng thể · 65 giây

**Chỉ vào:** ô client trên cùng → nhãn "REST / HTTP" → ba thẻ dịch vụ → đường cam OpenFeign → ô MySQL dưới cùng → dòng cam cuối slide.

> "Trên cùng là phía người dùng: Swagger UI và Postman, gọi thẳng HTTP tới từng dịch vụ, mỗi yêu cầu mang theo một token.
>
> Giữa là ba dịch vụ Spring Boot, mỗi dịch vụ một tiến trình và một cổng riêng. Auth và User ở cổng 8081 lo đăng nhập, cấp token và vai trò. Pitch ở cổng 8082 lo danh mục sân và đơn giá. Booking ở cổng 8083 nhận đơn đặt, tính tiền và chống trùng giờ.
>
> Mỗi dịch vụ sở hữu riêng một schema MySQL. Không ai được chạm vào cơ sở dữ liệu của dịch vụ khác; muốn biết dữ liệu bên kia thì phải hỏi qua API. Đó là đường màu cam này: Booking gọi sang Pitch bằng OpenFeign để lấy đơn giá.
>
> Nhóm em không dùng API Gateway, Eureka hay Kafka, vì với ba dịch vụ thì chúng chưa giải quyết vấn đề nào đang có. Hệ quả nhóm em chấp nhận là mã xác thực token bị lặp ở cả ba dịch vụ."

**Câu chuyển:** "Slide sau xin nói rõ hơn về cách ba dịch vụ phối hợp."

**Lưu ý:** Câu cuối là câu quan trọng nhất slide. Thầy rất hay hỏi "sao không dùng Gateway" — nói trước thì thành điểm cộng, để thầy hỏi thì thành điểm trừ.

---

### Slide 5 — Phân chia trách nhiệm và giao tiếp · 55 giây

**Chỉ vào:** thẻ "REST" bên trái → thẻ "OpenFeign" bên phải → bảng ba dòng ở dưới.

> "Hệ thống chỉ có đúng một kiểu giao tiếp: REST đồng bộ, nghĩa là gọi rồi đứng chờ trả lời. Không có hàng đợi sự kiện.
>
> Có hai hướng gọi. Bên trái là client hỏi dịch vụ. Điểm đáng nói là mỗi dịch vụ tự xác minh chữ ký token chứ không hỏi lại Auth Service. Nhờ vậy Auth chỉ cần sống lúc đăng nhập, và nó không thành cổ chai của cả hệ thống.
>
> Bên phải là dịch vụ hỏi dịch vụ. Trong cả hệ thống chỉ có đúng một lời gọi như vậy: Booking gọi Pitch để lấy đơn giá, và chỉ một chiều — Pitch không bao giờ gọi ngược lại.
>
> Bảng dưới là ranh giới dữ liệu: mỗi dịch vụ chỉ đọc và ghi đúng một schema của mình."

**Câu chuyển:** "Để cụ thể, em xin đi theo một đơn đặt sân thật."

---

### Slide 6 — Luồng đặt sân 450.000 đồng · 90 giây

**Chỉ vào:** ba cột trên đầu → từng mũi tên theo số 1, 2, 3, 4, 5 → khung kết luận dưới cùng.

> "Sơ đồ này đọc từ trên xuống theo thời gian. Ba cột dọc là ba bên tham gia: khách hàng, Booking Service và Pitch Service. Tình huống: sân 1 giá 300 nghìn một giờ, khách đặt từ chín giờ đến mười giờ ba mươi, tức một tiếng rưỡi.
>
> Bước một, khách gửi yêu cầu đặt sân tới Booking, kèm token. Booking xác minh chữ ký token, lấy ra userId và vai trò.
>
> Bước hai, Booking không tự biết giá sân, nên nó gọi OpenFeign sang Pitch Service hỏi thông tin sân số 1.
>
> Bước ba, Pitch trả về: giá 300 nghìn một giờ, trạng thái hoạt động. Nếu trạng thái là bảo trì, Booking sẽ dừng ngay ở đây và trả lỗi.
>
> Bước bốn là phần xử lý bên trong Booking, gồm ba việc liền nhau. Nhân một tiếng rưỡi với 300 nghìn, ra 450 nghìn. Kiểm tra khung giờ này đã có đơn nào giữ chưa. Rồi mới ghi đơn.
>
> Bước năm, Booking trả về mã 201, tổng tiền 450 nghìn, trạng thái chờ duyệt. Đơn lúc này đã nằm trong cơ sở dữ liệu, chờ chủ sân vào duyệt hoặc từ chối.
>
> Điểm em muốn nhấn là dòng cuối cùng: con số 450 nghìn do Booking tự tính sau khi đi hỏi Pitch, chứ không phải khách gửi lên. Nếu để khách gửi giá thì khách sửa được giá."

**Lưu ý:** Đây là slide 90 giây, dài nhất. Đi tay theo từng mũi tên, mỗi bước một nhịp. Nếu vội, gộp bước 2 và 3 thành một câu, nhưng **không được bỏ câu cuối** — đó là điểm thiết kế thầy dễ hỏi nhất.

**Nếu thầy chen vào "tại sao không để client gửi giá?":** trả lời ngắn — *"vì client nằm ngoài tầm kiểm soát của hệ thống, thưa thầy. Mọi dữ liệu ảnh hưởng tới tiền đều phải do server tự tra."*

---

### Slide 7 — Xử lý lỗi và nhất quán dữ liệu · 70 giây

**Chỉ vào:** bốn thẻ mã lỗi lần lượt → thẻ "Hai khách đặt cùng một giây" → thẻ "Lỗi được cô lập" → dòng cam cuối.

> "Nhóm em chia lỗi theo nguyên nhân, vì mỗi nguyên nhân dẫn tới một hành động khác nhau phía client.
>
> Sân không tồn tại thì trả 404. Pitch Service đã tắt thì trả 503, kèm thông báo thử lại sau. Còn hai trường hợp vi phạm nghiệp vụ — sân bảo trì và khung giờ đã có người đặt — thì trả 400.
>
> Bên dưới là câu trả lời cho câu hỏi ở slide hai. Booking giữ một khóa riêng cho từng sân, bọc cả việc kiểm tra trùng giờ và ghi đơn vào trong một khối, nên hai yêu cầu cùng một sân buộc phải xếp hàng lần lượt. Kết quả: đúng một đơn nhận 201, đơn còn lại nhận 400. Nhóm em đã chạy thật.
>
> Bên phải là một thực nghiệm khác: tắt hẳn Pitch Service thì đặt sân mới trả 503, nhưng xem lại đơn cũ vẫn trả 200. Một dịch vụ chết không kéo sập cả hệ thống.
>
> Và xin nói rõ giới hạn ở dòng cuối: khóa đó nằm trong bộ nhớ tiến trình, nên chỉ đúng khi chạy một bản Booking Service."

**Lưu ý:** Slide ăn điểm nhất. Hai chỗ phải nói rõ: **"đúng một đơn nhận 201"** và **"khóa nằm trong bộ nhớ nên chỉ đúng với một bản"**. Tự nêu giới hạn trước khi thầy tìm ra là cách ghi điểm mạnh nhất ở môn này.

**Nếu thầy hỏi "sao đặt trùng lại là 400 chứ không phải 409?":** *"409 đúng ngữ nghĩa hơn thưa thầy. Nhóm em chọn 400 cho mọi lỗi vi phạm nghiệp vụ để nhất quán, phân biệt bằng nội dung thông báo. Đổi sang 409 chỉ cần sửa một lớp ngoại lệ."*

---

### Slide 8 — Kết quả và giới hạn hiện tại · 50 giây

**Chỉ vào:** ba con số lớn → khung "Bốn phép kiểm còn lại" → hai cột "Đã đối chiếu" và "Chưa kiểm".

> "Nhóm em viết ba bộ Postman Collection chạy trên hệ thống thật: 60 request, 119 phép kiểm tự động, 115 đạt.
>
> Bốn phép kiểm còn lại thuộc nhóm kiểm thử mã 503, muốn chạy chúng thì phải tắt Pitch Service. Đó là điều kiện của chính ca kiểm thử, không phải lỗi hệ thống.
>
> Cột trái là những gì nhóm em đã đối chiếu trên hệ thống đang chạy: đặt sân liên dịch vụ với tổng tiền tính đúng, phân quyền ba vai trò, và bốn mã lỗi với dữ liệu thật ghi xuống đĩa.
>
> Cột phải là những gì chưa kiểm, xin nói thẳng: chạy nhiều bản Booking cùng lúc, chịu tải với số lượng người dùng lớn, và giao diện web cùng Docker Compose."

**Câu chuyển:** "Từ những giới hạn đó, nhóm em xác định ba việc cần làm tiếp."

**Lưu ý:** Dòng trắng cuối slide ghi "bốn vấn đề phát hiện khi chạy thật" — không cần đọc, nhưng phải biết để trả lời nếu thầy chỉ vào.

**Nếu thầy hỏi "vấn đề nào làm hỏng buổi demo?":** *"Thưa thầy, một ca kiểm thử chuyển sân số 1 sang bảo trì nhưng không trả lại trạng thái cũ. Chạy lần đầu thì đạt, từ lần thứ hai trở đi các ca đặt sân phía sau đều trượt. Nhóm em đã sửa cho ca đó tự tạo sân riêng để thao tác, không đụng vào dữ liệu mẫu."*

---

### Slide 9 — Hướng phát triển · 50 giây

**Chỉ vào:** ba khối 01, 02, 03 → khung kết luận dưới cùng.

> "Ba việc, xếp theo mức độ nghiêm trọng.
>
> Thứ nhất là bảo mật. Hiện cả ba dịch vụ cùng giữ một khóa bí mật, nên dịch vụ nào cũng tự phát hành được token quản trị. Chuyển sang RS256 thì chỉ Auth giữ khóa ký, hai dịch vụ còn lại chỉ xác minh. Kèm theo là HTTPS và Refresh Token.
>
> Thứ hai là độ tin cậy: đưa khóa chống trùng xuống tầng cơ sở dữ liệu bằng một ràng buộc duy nhất, để chạy được nhiều bản Booking.
>
> Thứ ba là vận hành: thêm API Gateway, đóng gói bằng Docker Compose và làm giao diện web.
>
> Ưu tiên số một là RS256, vì nó khắc phục hạn chế nghiêm trọng nhất hiện nay. Em xin hết. Kính mời thầy đặt câu hỏi."

**Lưu ý:** Nói "Em xin hết" rõ ràng rồi dừng hẳn, đứng yên. Đừng nói thêm, đừng cười trừ.

---

## C. Trả lời câu hỏi

**Công thức ba bước cho mọi câu hỏi:**

1. Nhắc lại câu hỏi bằng một cụm ngắn — *"Dạ, thầy hỏi về..."* (vừa cho mình nghĩ, vừa chắc là hiểu đúng)
2. Trả lời **kết luận trước**, lý do sau
3. Nếu có liên quan tới giới hạn đã biết, nói luôn: *"nhóm em có ghi điều này ở slide..."*

**Năm câu hay hỏi nhất, trả lời rút gọn:**

| Câu hỏi | Trả lời trong một hơi |
|---|---|
| Sao không dùng API Gateway? | "Với ba dịch vụ thì Gateway thêm một tầng phải chạy và gỡ lỗi mà chưa giải quyết vấn đề nào đang có. Nhóm em chấp nhận hệ quả là mã JWT lặp ba nơi, và đã đưa Gateway vào hướng phát triển ở slide 9." |
| Sao không dùng Kafka? | "Vì không có việc nào trong hệ thống chịu được chậm. Đặt sân phải trả lời ngay là được hay không, cả bốn bước đều phải xong trước khi trả lời khách." |
| Hai người đặt cùng lúc thì sao? | "Booking giữ khóa riêng cho từng sân, bọc cả bước kiểm tra trùng và ghi đơn vào một khối. Đúng một đơn nhận 201, đơn kia nhận 400. Nhóm em đã chạy thật." |
| Không có khóa ngoại thì dữ liệu sai thì sao? | "Việc kiểm chuyển từ cơ sở dữ liệu lên tầng mã nguồn: Booking phải gọi Pitch hỏi sân có tồn tại và còn hoạt động không. Sân sai thì nhận 404, sân bảo trì thì nhận 400." |
| Bốn phép kiểm trượt là lỗi gì? | "Không phải lỗi hệ thống, thưa thầy. Bốn ca đó kiểm mã 503, phải tắt Pitch Service mới chạy được. Chạy với hệ thống đầy đủ thì chúng đương nhiên không đạt." |

Giải thích đầy đủ hơn cho mười hai câu hỏi: xem [Phần 9 của bản lý thuyết](LY_THUYET_NEN_PitchOS.md).

**Nếu không biết câu trả lời:** *"Dạ, chỗ này nhóm em chưa kiểm, em không dám trả lời chắc. Em xin ghi lại và kiểm rồi báo lại thầy."* — Câu này được điểm cao hơn một câu trả lời đoán mò rất nhiều.

---

## D. Tránh nói những câu này

| Đừng nói | Nói thay bằng |
|---|---|
| "Em nghĩ là nó chạy được" | "Nhóm em đã chạy thử và kết quả là..." |
| "Cái này em chưa làm được" | "Việc này nhóm em chủ động để ngoài phạm vi vì..." |
| "Microservices thì nó hiện đại hơn" | "Nhóm em chọn microservices vì ba nghiệp vụ tách bạch rõ và bốn người làm song song được" |
| "Hệ thống này bảo mật tốt" | "Hệ thống dùng JWT và phân quyền theo vai trò, nhưng còn hạn chế là khóa bí mật dùng chung — nhóm em có ghi ở slide 9" |
| "Cái này chắc là do Spring tự lo" | "Phần này do Spring Security xử lý, cụ thể là..." |
| "Hệ thống chịu được nhiều người dùng" | **Đừng nói câu này.** Nhóm chưa kiểm tải, slide 8 đã ghi rõ |

**Nguyên tắc chung:** mọi con số và mọi khẳng định trên slide đều lấy từ lần chạy thật. Đừng thêm con số nào ngoài slide, và đừng khẳng định điều gì chưa kiểm. Slide đã tự nêu bốn giới hạn — giữ đúng giọng đó khi nói là đã đủ thuyết phục.
