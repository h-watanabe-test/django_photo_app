async function uploadToS3(file) {
  // Presigned URL取得
  const res = await fetch('/get-presigned-url/', {
    method: 'POST',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    body: new URLSearchParams({file_name: file.name})
  });
  const presigned = await res.json();

  // S3へアップロード
  const formData = new FormData();
  Object.entries(presigned.fields).forEach(([k, v]) => formData.append(k, v));
  formData.append('file', file);
  await fetch(presigned.url, {method: 'POST', body: formData});

  // メタデータをDjangoにPOST
  await fetch('/api/record-upload/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({file_name: file.name, s3_key: presigned.fields.key})
  });

  alert('アップロード完了');
}

// CSRFトークン取得用関数（Django公式推奨）
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
