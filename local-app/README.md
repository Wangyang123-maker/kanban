# 本地实时看板

这套方式以 Windows 电脑上的 Python 服务为唯一数据源：Excel 在电脑上上传和计算，手机、平板、Mac 和其他 Windows 电脑通过浏览器实时查看。

## 启动

双击 `start-local-dashboard.bat`。它会自动检查并启动 `serve.py`，打开本机看板，并显示手机访问地址。

手机与电脑连接同一个 Wi-Fi 时，在手机浏览器打开：

`http://电脑局域网IPv4地址:8017/`

手机端不需要安装 App，可以在 Safari/Chrome 中选择“添加到主屏幕”。跨网络访问时，安装并登录 Tailscale，然后使用脚本显示的 Tailscale 地址。

## 自动启动

右键 PowerShell，执行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install-autostart.ps1
```

## 检查

```powershell
.\healthcheck.ps1
```

## 重要说明

GitHub Pages 只保留公开静态快照；实时上传和数据处理必须使用本地地址。电脑需要保持开机和联网，手机才能实时查看。
