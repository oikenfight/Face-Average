// $(document).ready(function(){
//     console.log('hoge');
//
//
//     // 画像ファイルプレビュー表示
//     $('#face-image-form').on('change', 'input[type="file"]', function(e) {
//         alert('hoge ');
//         var file = e.target.files[0],
//             reader = new FileReader(),
//             $preview = $(".preview");
//
//         // 画像ファイル以外の場合は何もしない
//         if(file.type.indexOf("image") < 0){
//           return false;
//         }
//
//         reader.onload = (function(file) {
//             return function(e) {
//             $preview.empty();
//             $preview.append($('<img>').attr({
//                         src: e.target.result,
//                         width: "150px",
//                         class: "preview",
//                         title: file.name
//                     }));
//             };
//         })(file);
//
//         reader.readAsDataURL(file);
//     });
//
//     console.log('here');
//     var elm = $("#image-submit-button");
//     console.log(elm);
//
//     // 画像をアップロードする
//     $("#image-submit-button").one("click", function () {
//         console.log('clicked');
//         //クリックした要素のidをサーバに渡す
//         var formdata = new FormData($('#face-image-form').get(0));
//         $.ajax({
//             type: 'POST',
//             url: '{{ url_for("upload") }}',
//             data: formdata
//         })
//         .then(
//             function (data) {
//                 alert('アップロードが完了しました。');
//             },
//             function () {
//                 alert('アップロードに失敗しました。顔が２つ以上検出された可能性があります。');
//             }
//         );
//     });
// });
//
//
