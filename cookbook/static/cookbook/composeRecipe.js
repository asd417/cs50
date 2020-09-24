var stepCount = 1;
    document.addEventListener('DOMContentLoaded', function() {
        stepCount = 1;
        document.querySelector('#add_step').addEventListener('click',function() {
            nextstepCount = stepCount + 1;
            newstep = document.createElement('div');
            newstep.className = "card"
            newstep.innerHTML = `
            <div class="card-body">
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">Step ${nextstepCount}</span>
                    </div>
                    <textarea id='step${stepCount}' name='step${stepCount}' class="form-control" required></textarea>
                </div>
                
                <img src="" id='image${stepCount}' name='image${stepCount}' style="display:none">
                <button id='del_image${stepCount}' style="display:none">Delete Image</button>

                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text" id="inputGroupFileAddon01">Upload</span>
                    </div>
                    <div class="custom-file">
                        <input type="file" class="custom-file-input" id="inputGroupFile01" name="img${stepCount}" aria-describedby="inputGroupFileAddon01">
                        <label class="custom-file-label" for="inputGroupFile01 image${stepCount}">Choose an for the Step</label>
                    </div>
                </div>
            </div>`
            stepContainer = this.parentElement;
            stepContainer.insertBefore(newstep, this);
            stepCount += 1;
            document.querySelector('#stepcounter').value = stepCount;
        })

        document.querySelector('#remove_step').addEventListener('click',function() {
            if(stepCount > 1){
                stepCount -= 1
                stepContainer = this.parentElement;
                stepContainer.children[stepCount].remove();
            }
            document.querySelector('#stepcounter').value = stepCount;
        })
    })