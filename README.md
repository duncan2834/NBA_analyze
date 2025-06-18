# 🏀 NBA match analyze with YOLOv8 and ByteTrack, along with Fashion-CLIP
Project giúp phân tích dữ liệu trận đấu bóng rổ chỉ dựa trên hình ảnh cụ thể hơn là video đưa vào. Từ đó đưa ra thống kê các thông số của các cầu thủ, mỗi đội một cách tự động thay vì làm thủ công hoặc sử dụng
các công cụ khác. 

## Giới thiệu 
Dự án này là về phân tích một tình huống dài khoảng 10s trong 1 trận bóng rổ NBA như các cầu thủ đang thuộc team nào,
số lần ném, khu vực ném, số lần chuyền đúng và chuyền nhầm, phần trăm thời gian mỗi đội kiểm soát bóng.

## Tính năng 

- ✅ Sử dụng YOLOv8 + Bytetrack để track theo các cầu thủ cũng như quả bóng
- ✅ Sử dụng Fashion-CLIP để dựa trên bounding box của các cầu thủ nhận diện từ YOLOv8 để nhận diện màu áo(black_shirt and white_shirt), từ đó biết được cầu thủ được track ở team nào
- ✅ Sử dụng YOLOv8 segmentation để nhận diện khu vực paint, khu vực 2 điểm và khu vực 3 điểm. Từ vị trí của các cầu thủ được track, sẽ biết được cầu thủ đang ở khu vực nào, giúp cho việc nhận biết
  số lần ném 2, 3 điểm cũng như thống kê phạm vi hoạt động của các cầu thủ.

## 💻 Các thư viện sử dụng
- Supervision, ultralytics, transformers, OpenCV

## Dataset
- 1 tình huống ngắn trong 1 trận đấu NBA khoảng 10s
- Các cầu thủ, quả bóng, lưới rổ được gán nhãn thủ công trên Roboflow và huấn luyện bằng yolov8n với 100 epochs.
- Data được gán nhãn sẵn về khu vực trong sân được lấy từ Roboflow và huấn luyện bằng yolov8 seg với 100 epochs, accuracy trên 90%.

## Thiếu sót
- Các cầu thủ được track chưa quá hoàn hảo, nếu cầu thủ biến mất khỏi khung hình một lúc hoặc bị che khuất bởi cầu thủ khác một lúc đủ lâu thì sẽ bị gán track id mới. Từ đó gây khó khăn cho việc tính stats
cho từng cầu thủ riêng lẻ. Dự án mới dừng lại ở việc phân tích thông số theo đội. 


https://github.com/user-attachments/assets/e1ac9767-8f6d-4e51-8fec-a4eff3e88dec

