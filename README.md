Đề xuất mô hình mạng trên EVE-NG, sử dụng Netmiko Python để cấu hình và Ansible để quản lý các cấu hình
1. TRIỂN KHAI
3.1.	Cài đặt EVE-NG và các image mô phỏng.
	Chuẩn bị: VMWare Workstation Pro, WinSCP
Quá trình cài đặt EVE-NG trên nền tảng ảo hoá VMWare Workstation Pro và các image mô phỏng:
-	Bước 1: Tải file iso của EVE-NG trên trang chủ của EVE-NG 

Link: EVE-NG Iso Download
 
Hình 3 1: Sau khi download file iso EVE-NG
-	Bước 2: Cài đặt EVE-NG trên VMWare

 
Hình 3 2: Giao diện của VMWare Workstation Pro
 
Hình 3 3: File EVE-CE.ovf
Tạo Virtual Machine mới bằng cách nhấn vào Open a Virtual Machine và chọn đến file EVE-CE.ovf. Sau đó nhập tên và đường dẫn lưu trữ của máy ảo.

 
Hình 3 4: Mục Settings của máy ảo
Cấu hình đề nghị cho EVE-NG theo kinh nghiệm: Memory 12GB, Processors (CPU) 4, Hard Disk trên 40GB, Network Adapter là NAT và tick vào ô Virtualize Inter VT -x/EPT or AMD-V/RVI.

 
Hình 3 5: EVE-NG sau khi cài đặt
Truy cập vào Web UI của EVE-NG bằng cách truy cập đến URL được hiển thị trên màn hình là http://192.168.1.176/

 
Hình 3 6: Màn hình đăng nhập của EVE-NG
Đăng nhập với username là admin và password là eve
-	Bước 3: Thêm các image mô phỏng vào EVE-NG.
Tải các image để mô phỏng chức năng của các Router, Linux Server, Switch Layer 2, và Switch Layer 3. Lưu ý: các image mô phỏng chủ yếu được tải miễn phí từ cộng đồng của EVE-NG chia sẻ lại nên có thể nguồn tải sẽ không chính thống từ EVE-NG nhưng vẫn đảm bảo được các tính năng cần thiết.
Link download cho các image tại đây Image
 
Hình 3 7: Đăng nhập vào WinSCP
Đăng nhập vào WinSCP với Hostname là 192.168.1.176, Port là 22, Username root và Password là eve
Tham khảo cách thêm các image từ tài liệu của EVE-NG ở đường dẫn Add Image Router Switch và Add Linux Server. Sau khi thêm thành công sẽ được như hình 3-8

 
Hình 3 8: Giao diện của WinSCP sau khi thêm image
Sau khi thêm xong các image, truy cập vào Web UI của EVE-NG tiến hành thiết kế mô hình mạng như đã đề xuất. 
