function addNewPost() {
  document.getElementById('add_new_post').style.display = "block";
  document.getElementById('btn_add_new_post').style.display = "none";
}

function follow(user_id, x) {
  fetch('/follow/' + user_id, {
    method: 'PUT',
    body: JSON.stringify({
      [x]: user_id
    })
  })
  .then(response => response.json())
  .then(result => {
    document.querySelector('#num_followers').innerHTML = 'Followers: ' + result.followers_counter;
    console.log(result.message)
  });
}


function vote(elem, user_id, x) {
    let post_id = elem.parentNode.id;
      fetch('/post/' + post_id , {
        method: 'PUT',
        body: JSON.stringify({
          [x]: user_id
        })
      })
      .then(response => response.json())
      .then(result => {
          document.querySelector("#likes-counter-" + post_id).innerHTML = result.likes_counter;
          console.log(result);
      });
}

function editPost(postId) {

  const editPostForm = document.createElement('Form');
    editPostForm.id = 'edit-post-form';
    editPostForm.className = 'form-group';
    let text = document.querySelector('#post' + postId + '-text').innerHTML;
    editPostForm.value = document.querySelector('#post' + postId + '-text').innerHTML;
  document.querySelector('#post' + postId + '-text').replaceWith(editPostForm);

  const editPostArea = document.createElement('input');
    editPostArea.id = 'edit-post-area';
    editPostArea.className = "form-control"
    editPostArea.value = text;

    const butSub = document.createElement('Button');
    butSub.id = "but-sub";
    butSub.className = 'btn btn-primary';
    butSub.type ="submit";
    butSub.innerHTML = 'Save';
    document.querySelector('#edit-post-form').append(editPostArea);
    document.querySelector('#edit-post-form').append(butSub);
    document.querySelector('#but-sub').addEventListener('click', (event) => {

    let newtext = document.querySelector('#edit-post-area').value;
    console.log(newtext)

      fetch('/edit_post/' + postId, {
        method: 'PUT',
        body: JSON.stringify({
          'post': newtext
        })
      })
      .then(response => response.json())
      .then(result => {

          const newTextDiv = document.createElement('div');
          newTextDiv.id = 'post' + postId + '-text';
          newTextDiv.innerHTML = newtext;
          document.querySelector('#edit-post-form').replaceWith(newTextDiv);
          console.log(result);

      });
      event.preventDefault();
  });
}
