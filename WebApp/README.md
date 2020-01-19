# WebApp Crawling

WebApp Crawling là một trang mạng giúp người môi giới bất động sản thông qua việc thể hiện 3 thông tin quan trọng nhất: Danh sách người mua bán nhà đất, Biểu đồ dự đoán giá cả và Bản đồ phổ biến của nhà đất.

**ĐẶC ĐiỂM:** Hiện tại trang mạng đang sử dụng Node.js phiên bản v10.16.0 và thêm môn số các thư viện cụ thể. Vì thế. khi cài đặt / chạy webapp, vui lòng kiểm tra phần Hướng dẫn cài đặt bên dưới nếu đây là lần đầu bạn sử dụng WebApp Crawling

**LƯU Ý:** Dự án vẫn trong giai đoạn thử nghiệm và sẽ còn được tiếp tục phát triển.

## Hướng dẫn cài đặt

- [Cài đặt node.js phiên bản mới và ổn định nhất](https://nodejs.org/en/)
- Sau khi đã cài đặt thành công Node.js (Lưu ý nhỏ: Đường dẫn dùng để cài đặt Node.js tuyệt đối không được có dấu cách), hãy mở CMD nếu đã thêm Node.js vào path hoặc mở terminal dành riêng cho Node.js và cài đặt npm để có thể thêm các thư viện ngoài.

        npm install

- Tiếp đến, truy cập file package.json để kiểm tra các thư viện mà WebApp Crawling đang sử dụng để tải về. Ví dụ, trong file package.json có ghi express thì express đang được trang mạng sử dụng và cách cài đặt như sau:

        npm install express

- Cuối cùng, sau khi đã cài đặt xong tất cả thư viện thì bạn có thể cài thêm nodemon để có thể cập nhật server liên tục (hoặc chỉ dùng node cũng không sao)

        npm install nodemon

## Chạy chương trình

- Truy cập folder bin bằng terminal và chạy dòng lệnh dưới đây để khởi động webapp

        nodemon www


## Các lỗi thường gặp

- Nếu báo lỗi là port đang bận thì bạn hãy vào file www và chỉnh port khác.

## Cài đặt API phân loại text

run api :
	cài docker, python (>3.0)
	ùng command prompt trỏ tới thư mục "tag_serice" chạy các lệnh sau:
		docker build -t tag_service .

		docker rm -f tag_service_July18

		docker run -p 3005:5000 --name tag_service_July18 --restart always -t tag_service bash -c "chmod 777 ./scripts/run_service.sh && ./scripts/run_service.sh"

run project:
		cài nodejs
		cài các package trong file package.json của folder "WebApp" bằng lệnh sau:
			npm install + [tên package]
		cài nodemon : npm install nodemon
		trỏ tới folder "WebApp" run : nodemon bin/www
