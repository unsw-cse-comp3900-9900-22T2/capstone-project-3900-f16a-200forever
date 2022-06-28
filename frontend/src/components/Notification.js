import { notification } from "antd";

const openNotification = (msg) => {
  notification.open({
    message: msg["title"],
    description: msg["content"],
    duration: 3,
  });
};

export default openNotification;
