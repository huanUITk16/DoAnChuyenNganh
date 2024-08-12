## Mục đích của đề tài

Mục đích của dồ án này là đề xuất và triển khai một mô hình mạng ba lớp
(Three-Layer Hierarchical Model in Cisco) trên môi trường mô phỏng
EVE-NG, bao gồm lớp truy cập (Access Layer), lớp phân phối (Distribution
Layer) và lớp lõi (Core Layer). Đồ án này sẽ sử dụng các công cụ tự động
hoá như Netmiko Python để cấu hình các thiết bị mạng và Ansible để quản
lý các tác vụ cấu hình. Cụ thể, đồ án nhằm đạt được các mục tiêu sau:

- **Thiết kế và mô phỏng một mô hình mạng ba lớp trên EVE-NG**: Xây dựng
  và cấu hình các thiết bị mạng tương ứng cho từng lớp.

- **Sử dụng Netmiko Python**: Tự động hoá việc cấu hình các thiết bị
  mạng thông qua script Python sử dụng thư viện Netmiko.

- **Quản lý cấu hình bằng Ansible**: Tích hợp Ansible để quản lý và thực
  thi các tác vụ cấu hình trên các thiết bị mạng một cách hiệu quả.

- **Đánh giá khả năng dự phòng của hệ thống mạng**: Thực hiện các kịch
  bản gặp lỗi để đánh giá khả năng dự phòng và tính ổn định của hệ thống
  mạng.

## Đối tượng nghiên cứu

Đối tượng nghiên cứu trong đồ án này bao gồm:

- **Thiết bị mạng**: Các thiết bị như switch và router thuộc các lớp
  truy cập, phân phối và lõi trong mô hình mạng ba lớp.

- **Các công cụ tự động hoá**:

> **+ Netmiko**: Một thư viện của Python mã nguồn mở cho phép tự động
> hoá việc cấu hình thiết bị mạng thông qua giao thức SSH.
>
> **+** **Ansible**: Một công cụ tự động hoá mã nguồn mở dùng để quản lý
> cấu hình và thực thi các tác vụ trên các thiết bị mạng.

- **Công nghệ và các giao thức mạng**: Các giao thức và công nghệ mạng
  như VLAN, STP, OSPF, HSRP, NAT sử dụng trong việc cấu hình mô hình
  mạng ba lớp.

# TỔNG QUAN

## Các công cụ và môi trường

### EVE-NG


EVE-NG là một công cụ mô phỏng mạng cung cấp giao diện người dùng thông
qua trình duyệt. Người dùng có thể tạo các node mạng từ một thư viện các
tempalte sẵn có, kết nối chúng lại với nhau và cấu hình chúng. Người
dùng chuyên nghiệp hoặc quản trị viên có thể thêm các image phần mềm vào
thư viện và tạo các mẫu các thiết bị mạng tùy chỉnh để hỗ trợ hầu hết
các mô hình lab.

EVE-NG hỗ trợ cấu hình nhiều hypervisors trên một máy ảo. Nó chạy phần
mềm thiết bị mạng thương mại trên Dynamips và IOU và chạy các thiết bị
mạng khác, chẳng hạn như bộ định tuyến router mã nguồn mở, trên QEMU.

EVE-NG là một dự án nguồn mở và mã nguồn EVE-NG được đăng trên GitLab.

### Ansible


Ansible là một công cụ tự động hóa mã nguồn mở do Red Hat phát triển,
giúp quản lý cấu hình, triển khai ứng dụng và tự động hóa các tác vụ
mạng. Ansible sử dụng file YAML để viết các playbook, cho phép mô tả các
tác vụ một cách dễ hiểu và dễ bảo trì.


Netmiko là một thư viện Python mã nguồn mở được phát triển bởi Kirk
Byers. Thư viện này cung cấp một giao diện đơn giản và nhất quán để tự
động hóa các tác vụ quản lý và cấu hình thiết bị mạng.

## Mô mình mạng đề xuất

![image4](https://github.com/user-attachments/assets/c7aba1fa-b691-4aae-808c-b0a5bd1b5c3c)


Mô hình mạng được thiết kế theo kiến trúc 3 lớp của Cisco bao gồm lớp
kết nối (Access Layer), lớp phân phối (Distribution Layer) và lớp lõi
(Core Layer) với các thiết bị mô phỏng như sau:

- **2 Router Gateway ở Core Layer**: chịu trách nhiệm vận chuyển dữ liệu
  tốc độ cao giữa các phần khác nhau của mạng. Đây là xương sống của
  mạng, cung cấp khả năng ra Internet của mô hình mạng. Trong mô hình, 2
  router này sẽ chạy song song và khi 1 router bị sự cố, router còn lại
  sẽ làm backup cho router đã bị down.

- **2 Core Switch Layer 3 ở Distribution Layer**: kết nối các thiết bị
  giữa lớp Access và lớp Core. Thực hiện các chức năng định tuyến, phân
  phối IP đến các host trong LAN ảo (VLAN). Ở mô hình trên, Core 1 chịu
  trách nhiệm phân phối IP tự động (DHCP Pool) đến 2 VLAN 10 và 20 đồng
  thời cũng là thiết bị hoạt động chính để traffic có thể đến Core
  Layer. Core 2 là backup cho Core 1 khi Core 1 gặp sự cố.

- **2 Access Switch Layer 2 ở Access Layer:** cung cấp kết nối mạng cho
  các thiết bị như máy tính, điện thoại IP, và các thiết bị đầu cuối
  khác. Access 1 kết nối với VLAN 10 và Access 2 kết nối với VLAN 20.

- **1 máy ảo Linux:** triển khai Ansible trên máy ảo này để thực hiện
  các tác vụ cấu hình (Tasks) cho toàn bộ mô hình mạng.

- **Internet:** đóng vai trò là môi trường mạng public, mục đích để cho
  các thiết bị trong mạng LAN có thể giao tiếp được với bên ngoài

## Cơ sở lý thuyết

### Các giao thức mạng sử dụng

#### Network Address Translation (NAT)

NAT là một phương thức dùng để ánh xạ địa chỉ IP từ một không gian địa
chỉ này sang một không gian địa chỉ khác. NAT thường được sử dụng để cho
phép nhiều thiết bị trong một mạng cục bộ (LAN) sử dụng một địa chỉ IP
công cộng duy nhất để truy cập Internet. Điều này giúp tiết kiệm địa chỉ
IP và bảo vệ mạng nội bộ khỏi các cuộc tấn công từ bên ngoài.

#### Open Shortest Path First (OSPF)

OSPF là một giao thức định tuyến liên miền theo trạng thái liên kết được
sử dụng rộng rãi trong các mạng lớn và phức tạp. OSPF hoạt động bằng
cách xây dựng một bản đồ topo của mạng và tính toán đường đi ngắn nhất
đến từng mạng con bằng thuật toán Dijkstra. OSPF hỗ trợ cân bằng tải và
cung cấp khả năng hội tụ nhanh khi có thay đổi trong cấu trúc mạng.

#### Virtual Local Area Network (VLAN)

VLAN là một kỹ thuật chia mạng LAN vật lý thành nhiều mạng ảo độc lập.
Mỗi VLAN hoạt động như một mạng LAN riêng biệt, giúp cải thiện hiệu suất
mạng, tăng cường bảo mật và quản lý dễ dàng hơn. VLAN cho phép các thiết
bị trên cùng một VLAN giao tiếp trực tiếp với nhau mà không cần đi qua
router.

#### VLAN Trunking Protocol (VTP)

VTP là một giao thức quản lý VLAN được sử dụng để truyền thông tin cấu
hình VLAN trong toàn bộ mạng chuyển mạch (switching network). VTP cho
phép các switch tự động cập nhật cấu hình VLAN từ một switch trung tâm
(server) đến các switch khác (client), giúp đơn giản hóa việc quản lý và
triển khai VLAN trong một hệ thống lớn.

#### Rapid Spanning Tree Protocol (RSTP)

RSTP là một phiên bản cải tiến của giao thức Spanning Tree Protocol
(STP), được thiết kế để cung cấp sự hội tụ nhanh hơn trong trường hợp có
sự thay đổi trong topo mạng. RSTP giúp ngăn chặn các vòng lặp trong mạng
chuyển mạch bằng cách tạo ra một cây tối thiểu kết nối tất cả các switch
trong mạng. RSTP có khả năng phát hiện và khôi phục nhanh chóng khi có
sự cố xảy ra, giảm thiểu thời gian downtime.

#### Hot Standby Router Protocol (HSRP)

HSRP là một giao thức của Cisco được thiết kế để cung cấp khả năng
chuyển đổi dự phòng (redundancy) cho các router trong mạng. HSRP cho
phép một nhóm các router hoạt động cùng nhau để tạo ra một router ảo duy
nhất. Nếu router chính (active) bị lỗi, một router dự phòng (standby) sẽ
nhanh chóng tiếp quản vai trò của router chính, đảm bảo mạng vẫn hoạt
động liên tục và không bị gián đoạn.

# TRIỂN KHAI

## Cài đặt EVE-NG và các image mô phỏng.

- Chuẩn bị: VMWare Workstation Pro, WinSCP

Quá trình cài đặt EVE-NG trên nền tảng ảo hoá VMWare Workstation Pro và
các image mô phỏng:

- Bước 1: Tải file iso của EVE-NG trên trang chủ của EVE-NG

Link: [EVE-NG Iso Download](https://www.eve-ng.net/index.php/download/)

![image5](https://github.com/user-attachments/assets/d101746f-222e-4775-a45d-2468c3ef617c)


- Bước 2: Cài đặt EVE-NG trên VMWare

![image6](https://github.com/user-attachments/assets/7cdc7274-cc24-4309-887e-bf02413b771c)

![image7](https://github.com/user-attachments/assets/9e8bf91e-0b48-4252-b319-955374d179e3)


Tạo Virtual Machine mới bằng cách nhấn vào Open a Virtual Machine và
chọn đến file EVE-CE.ovf. Sau đó nhập tên và đường dẫn lưu trữ của máy
ảo.

![image8](https://github.com/user-attachments/assets/90fc457e-39d0-41ad-bcea-9dab4091a591)


Cấu hình đề nghị cho EVE-NG theo kinh nghiệm: Memory 12GB, Processors
(CPU) 4, Hard Disk trên 40GB, Network Adapter là NAT và tick vào ô
Virtualize Inter VT -x/EPT or AMD-V/RVI.

![image9](https://github.com/user-attachments/assets/18e83721-9eaf-450f-9edc-bd80e1fa4b9f)


Truy cập vào Web UI của EVE-NG bằng cách truy cập đến URL được hiển thị
trên màn hình là <http://192.168.1.176/>

![image10](https://github.com/user-attachments/assets/25479561-a82f-4f52-acb0-260672ec0318)


Đăng nhập với username là **admin** và password là **eve**

- Bước 3: Thêm các image mô phỏng vào EVE-NG.

Tải các image để mô phỏng chức năng của các Router, Linux Server, Switch
Layer 2, và Switch Layer 3. Lưu ý: các image mô phỏng chủ yếu được tải
miễn phí từ cộng đồng của EVE-NG chia sẻ lại nên có thể nguồn tải sẽ
không chính thống từ EVE-NG nhưng vẫn đảm bảo được các tính năng cần
thiết.

Link download cho các image tại đây
[Image](https://drive.google.com/drive/folders/1m77D6YYN2FJdJO2w2f9kBA94n-K4044j?usp=sharing)

![image11](https://github.com/user-attachments/assets/39f7ed81-411c-49cf-96ce-88c1c16c278c)


Đăng nhập vào WinSCP với Hostname là 192.168.1.176, Port là 22, Username
root và Password là eve

Tham khảo cách thêm các image từ tài liệu của EVE-NG ở đường dẫn [Add
Image Router
Switch](https://www.eve-ng.net/index.php/documentation/howtos/howto-add-cisco-iol-ios-on-linux/)
và [Add Linux
Server](https://www.eve-ng.net/index.php/documentation/howtos/howto-create-own-linux-host-image/%20).
Sau khi thêm thành công sẽ được như hình dưới

![image12](https://github.com/user-attachments/assets/36d533fe-af78-4605-b8c3-631cd379f6b3)


Sau khi thêm xong các image, truy cập vào Web UI của EVE-NG tiến hành
thiết kế mô hình mạng như đã đề xuất.



## Cài đặt thư viện Netmiko Python trên Linux Server

- Bước 1: Cập nhật hệ thống bằng câu lệnh:

sudo apt update

sudo apt upgrade -y

- Bước 2: Cài đặt Python và Pip

sudo apt install python3 python3-pip -y

- Bước 3: Cài đặt Netmiko

pip3 install netmiko

- Bước 4: Kiểm tra cài đặt bằng cách tạo 1 file python và import Netmiko
  vào, nếu chạy ra được như hình 3-13 tức là cài đặt thành công

![image17](https://github.com/user-attachments/assets/ab8c3c7f-b955-4a14-ba2d-271475184e78)


## Cài đặt Ansible

- Bước 1: Cập nhật hệ thống bằng câu lệnh:

sudo apt update

sudo apt upgrade -y

- Bước 2: Cài đặt Ansible bằng câu lệnh:

sudo apt install ansible -y

- Bước 3: Kiểm tra phiên bản của Ansible

![image18](https://github.com/user-attachments/assets/ff9f57c7-da9c-43f1-886d-3744f9a12d5b)

## Viết playbook cho Ansible

Viết các file yml trong Linux Server để chạy các file Script Python

![image19](https://github.com/user-attachments/assets/932c23d8-2068-4007-8a61-3a6e67b2ecbd)

![image20](https://github.com/user-attachments/assets/54a898e4-f2f0-477b-9be3-0213b86d2184)



Để có thể dùng ansible để thực hiện các tác vụ lên thiết bị, phải định
nghĩa các thông số cần thiết của thiết bị bao gồm địa chỉ IP, user,
password. Các thiết bị có thể được gom nhóm lại như trong file hosts như
là Routers, Cores, Accesses

![image21](https://github.com/user-attachments/assets/f7b2cd03-cb8a-4f9f-84b4-c34d028af30d)



Các thành phần của file yml:

- 'name': tên của playbook là Core config

- 'hosts': định nghĩa các đối tượng mà playbook được áp dụng các tác vụ,
  ở đây là nhóm "Cores" đã định nghĩa trong file hosts

- 'gather_facts': tắt việc thu thập các thông tin về hệ thống mặc định
  của Ansible. Do đây là thiết bị mạng nên không cần thiết.

- 'connection': chỉ định loại kết nối, ở đây là 'network_cli' để giao
  tiếp với thiết bị

- 'ansible_network_os': chỉ định hệ điều hành của thiết bị mạng, ở đây
  là ios

- 'ansible_user': username của thiết bị mạng là admin

- 'ansible_password': password của thiết bị mạng là cisco

- 'ansible_become': cho phép thực hiện các tác vụ nâng cao

- 'ansible_python_interpreter': đường dẫn đến trình thông dịch Python, ở
  đây có đường dẫn là '/usr/bin/python'

- 'ansible_ssh_timeout': thời gian chờ cho kết nối SSH là 60 giây

- 'ansible_builtin_script': module của ansible để chạy một file script

- 'cmd': đường dẫn đến file script, ở đây là
  '/etc/ansible/playbook/script/Core_configuration.py'

- 'executable': đường dẫn đến trình thông dịch Python

- 'register': Lưu kết quả của nhiệm vụ vào biến result

![image22](https://github.com/user-attachments/assets/e6aa2816-fc12-4254-b37b-7b5e2c1d1151)


Chạy các file yml bằng lệnh 'ansible-playbook \[tên file.yml\]' dưới
quyền root sẽ cho ra kết quả là các thiết bị đã có sự thay đổi trong cấu
hình và các tasks được thực hiện thành công.

Tham khảo thêm các file yml khác tại đường dẫn này:

Link: <https://github.com/huannv2973/netmiko-configuration>

![image23](https://github.com/user-attachments/assets/d2d920ee-c165-4ea6-9ff4-2b8b32aa7667)

> Hình 3‑19: Kiểm tra các cấu hình sau khi chạy Ansible

# KIỂM THỬ MÔ HÌNH

## Viết các kịch bản của mô hình mạng

| Thiết bị | Interface | IP Address | Default Gateway |
|:--:|:--:|:--:|:--:|
| Router Gateway 1 | E0/2 | 192.168.1.177/24 |  |
|  | E0/1 | 172.16.12.2/24 |  |
|  | E0/0 | 172.16.10.1/24 |  |
| Router Gateway 2 | E0/2 | 192.168.1.178/24 |  |
|  | E0/1 | 172.16.14.1/24 |  |
|  | E0/0 | 172.16.15.5/24 |  |
| Switch Core 1 | E3/0 | 192.168.1.189/24 |  |
|  | VLAN 10 | 192.168.10.5/24 |  |
|  | VLAN 20 | 192.168.20.5/24 |  |
|  | E0/2 | 172.16.10.2/24 |  |
|  | E0/3 | 172.16.14.2/24 |  |
| Switch Core 2 | E3/0 | 192.168.1.190/24 |  |
|  | VLAN 10 | 192.168.10.6/24 |  |
|  | VLAN 20 | 192.168.20.6/24 |  |
|  | E0/2 | 172.16.15.6/24 |  |
|  | E0/3 | 172.16.12.1/24 |  |
| DHCP Pool cho các VLAN (Switch Core 1) | VLAN 10 | 192.168.10.0/24 |  |
|  | VLAN 20 | 192.168.20.0/24 |  |
| Switch Access 1 | E3/0 | 192.168.1.191/24 |  |
| Switch Access 2 | E3/0 | 192.168.1.192/24 |  |
| VPC10 |  | 192.168.10.7/24 | 192.168.10.1/24 |
| VPC20 |  | 192.168.20.7/24 | 192.168.20.1/24 |


Để có thể dùng Netmiko để SSH và đẩy các lệnh cấu hình vào thiết bị thì
cần phải bật chế độ SSH và cấp một địa chỉ IP động trên thiết bị.

![image24](https://github.com/user-attachments/assets/691cff7d-6bc9-4143-a773-5b1a150ecc29)


<![image25](https://github.com/user-attachments/assets/ae41507f-1f72-4dfe-848d-5d8f31ca22fd)

![image26](https://github.com/user-attachments/assets/a96f088b-0384-49b6-89a1-327683dbd738)

Để dễ quản lý và và cấu hình thì sẽ chia thành các file tương ứng cho
từng lớp của mô hình mạng như là Gateway_configuration (lớp Core),
Core_configuration (lớp Distribution) và Access_configuration (lớp
Access).

![image27](https://github.com/user-attachments/assets/faa06b35-e7f7-4663-882a-b0d750be3166)

Định nghĩa các thiết bị sẽ SSH đến để thực hiện cấu hình bao gồm:
device_type, IP, username, password và các tuỳ chọn khác để hỗ trợ cho
việc chạy cấu hình. session_log để xuất ra các file log dễ theo dõi quá
trình cấu hình.

![image28](https://github.com/user-attachments/assets/fdc0f301-19a8-491a-82a3-9dcc92fb1884)


![image29](https://github.com/user-attachments/assets/645ed5c6-5a85-42ee-be90-bd09588df082)


![image30](https://github.com/user-attachments/assets/aa4ce19a-504f-4708-850b-8bd3a1a3f393)

Sau khi cấu hình xong sẽ xuất ra thông báo 'Config successfully !'

![image31](https://github.com/user-attachments/assets/fd935828-7183-4778-9806-66a14d902eb8)

Kiểm tra cấu hình trên thiết bị

Chạy lệnh 'show run' trên thiết bị và thấy rằng các cấu hình đã được
thêm vào từ file config bằng Netmiko.

![image32](https://github.com/user-attachments/assets/d13c58d3-8f15-4950-b8a9-6bf25ca82ef7)

File log các cấu hình được đẩy vào thiết bị

Tham khảo thêm các file config các thiết bị còn lại tại đường dẫn này:

Link: <https://github.com/huannv2973/netmiko-configuration.git>

## Trường hợp 1: Switch Core 1 bị shutdown

**Trước khi bị SHUTDOWN:**

![image33](https://github.com/user-attachments/assets/752650e3-db10-4475-b522-8cdccfaa4aac)


Trước khi bị Shutdown, trạng thái của Core 1 là Active cho VLAN 10 và 20

![image34](https://github.com/user-attachments/assets/9f6e128d-622d-4656-bb0d-8950447e78e5)

Trên Core 2 sẽ là trạng thái Standby (chờ) cho 2 VLAN 10 và 20

![image35](https://github.com/user-attachments/assets/015c4f29-e1f2-4837-b1bc-0c41a4d0d02c)

Trace 8.8.8.8 trên VPC thuộc VLAN 10

- Trên VPC thuộc VLAN 10, thực hiện xin địa chỉ IP từ IP DHCP Pool được
  cấu hình trên Switch Core 1. Sau khi được cấp địa chỉ IP, VPC sẽ có
  địa chỉ là 192.168.10.7/24 và default-gateway là 192.168.10.1

- Sau đó, thực hiện lệnh trace đến DNS Server 8.8.8.8 của Google thì
  đường đi của VPC như sau: VPC10 -\> Switch Core 1 -\> Router Gateway 2
  -\> Internet

**Sau khi bị SHUTDOWN:**

![image36](https://github.com/user-attachments/assets/3553d013-b1f2-4968-b27d-b713b9ef63c1)

Sau khi shutdown Core 1, Core 2 sẽ chiếm quyền

![image37](https://github.com/user-attachments/assets/94fe0f75-9183-46cf-9529-3fce9e539328)
Thực hiện trace trên VPC 10

Sau khi trace đến 8.8.8.8, đường đi của traffic đã có sự thay đổi, VPC
-\> Switch Core 2 -\> Router Gateway 2 -\> Internet

## Trường hợp 2: Router Gateway 1 bị shutdown

**Trước khi bị SHUTDOWN**

![image38](https://github.com/user-attachments/assets/26c10532-6b1d-48c2-b181-7b882a56ab91)
Trace 8.8.8.8 trên VPC10

Đường đi của traffic sẽ là: VPC10 -\> Switch Core 1 -\> Router Gateway 1
-\> Internet

**Sau khi bị SHUTDOWN**

![image39](https://github.com/user-attachments/assets/cdc82663-6df8-49b2-b253-bcc343c309ea)

Trace 8.8.8.8 trên VPC10

Đường đi của traffic có thay đổi như sau: VPC10 -\> Switch Core 1 -\>
Router Gateway 2 -\> Internet

# TỔNG KẾT

## So sánh giữa 2 hình thức cấu hình

| Kiểu cấu hình | CLI | Netmiko |
|:--:|:--:|:--:|
| Cách thức sử dụng | Thao tác thủ công, tiêu tốn thời gian, khả năng mắc lỗi cao | Tự động hoá, tiết kiệm thời gian và giảm sai sót |
| Độ linh hoạt và khả năng mở rộng | Linh hoạt, khó mở rộng | Linh hoạt và dễ mở rộng |
| Bảo mật | Kết nối trực tiếp, quản lý thủ công | Kết nối thông qua thư viện, dễ quản lý |
| Tính dễ dàng sử dụng | Đòi hỏi kiến thức sâu và học tập lâu | Dễ học và tái sử dụng nếu đã biết đến Python |

> Bảng 2: Bảng so sánh 2 kiểu cấu hình

## Kết luận

### Những công việc mà nhóm đã thực hiện được

- Thực hiện đề xuất và triển khai một mô hình mạng 3 lớp cơ bản

- Sử dụng Netmiko để cấu hình

- Sử dụng Ansible để quản lý các cấu hình

- Thực hiện các kịch bản lỗi của thiết bị

- So sánh và hiểu được 2 hình thức cấu hình cho mô hình mạng là truyền
  thống bằng lệnh CLI và tự động bằng Script Python

### Phương hướng phát triển

- Mở rộng các kịch bản mô phỏng với quy mô lớn hơn và phức tạp hơn

- Nghiên cứu các xu hướng mới hiện nay như Network as Code (NaC) và
  Infrastructure as Code (IaC) trong lĩnh vực triển khai mô hình mạng và
  quản lý cấu hình

## Tài liệu tham khảo

\[1\]

“Documentation.” <https://www.eve-ng.net/index.php/documentation/>

\[2\]

I. Ansible, “Ansible Documentation,” *Ansible.com*, 2019.
<https://docs.ansible.com/>

\[3\]

“Python for Network Engineers - Netmiko Library,” *pynet.twb-tech.com*.
<https://pynet.twb-tech.com/blog/netmiko-python-library.html>

‌\[4\]

Charles Judd, “Using Ansible Automation with EVE-NG,” *YouTube*, Jul.
29, 2021.
[https://www.youtube.com/watch?v=H8yg7XnNfas](https://www.youtube.com/watch?v=H8yg7XnNfas%20)
(accessed Jun. 29, 2024).

\[5\]

“Netmiko Tutorials For Network Engineers(12 Videos) -
YouTube,” *www.youtube.com*.
[https://youtube.com/playlist?list=PLOocymQm7YWbfFxETimO1VmgtVGRnEGyE&si=bQn3S0260ZSoU9a8](https://youtube.com/playlist?list=PLOocymQm7YWbfFxETimO1VmgtVGRnEGyE&si=bQn3S0260ZSoU9a8%20)
(accessed Jun. 29, 2024).

## Demo sản phẩm

Trình tự của demo:

- Kích hoạt SSH trên các thiết bị, DHCP IP cho các thiết bị từ internet

- Chạy Ansible từ Linux Server

- Kiểm tra cấu hình trên thiết bị, chạy các kịch bản mô hình bị lỗi và
  traceroute các thiết bị ra ngoài Internet

Link demo:
[DEMO](https://drive.google.com/file/d/1EKNxgSNIDIhRcroLzb7rAuVejy7blNkq/view?usp=sharing)

‌
