/**
 * 学生管理系统 - 主JavaScript文件
 * 苹果风格UI交互
 */

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function () {
    // 初始化导航栏滚动效果
    initNavbarScroll();

    // 初始化下拉菜单
    initDropdowns();

    // 初始化模态框
    initModals();

    // 初始化表格hover效果
    initTableHover();

    // 初始化页面转场动画
    initPageTransitions();

    // 初始化表单验证
    initFormValidation();

    // 初始化背景设置面板
    initBackgroundSettings();

    // 初始化移动端导航
    initMobileNav();

    // 初始化拖放排序功能
    initSortable();

    // 初始化页面性能优化
    optimizePageLoad();
});

/**
 * 导航栏滚动效果
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 10) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
}

/**
 * 下拉菜单初始化
 */
function initDropdowns() {
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            const parent = this.closest('.dropdown');
            const menu = parent.querySelector('.dropdown-menu');

            // 关闭其他已打开的下拉菜单
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                if (openMenu !== menu) {
                    openMenu.classList.remove('show');
                }
            });

            // 切换当前下拉菜单
            menu.classList.toggle('show');
        });
    });

    // 点击页面其他区域关闭下拉菜单
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
}

/**
 * 模态框初始化
 */
function initModals() {
    const modalTriggers = document.querySelectorAll('[data-toggle="modal"]');

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('data-target');
            const modal = document.querySelector(targetId);

            if (modal) {
                openModal(modal);
            }
        });
    });

    // 关闭按钮事件
    document.querySelectorAll('.modal-close, [data-dismiss="modal"]').forEach(closeBtn => {
        closeBtn.addEventListener('click', function () {
            const modal = this.closest('.modal-backdrop');
            closeModal(modal);
        });
    });

    // 点击背景关闭模态框
    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
        backdrop.addEventListener('click', function (e) {
            if (e.target === this) {
                closeModal(this);
            }
        });
    });

    // ESC键关闭模态框
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal-backdrop.show');
            if (openModals.length) {
                closeModal(openModals[openModals.length - 1]);
            }
        }
    });
}

/**
 * 打开模态框
 */
function openModal(modal) {
    const backdrop = modal.closest('.modal-backdrop') || modal;
    backdrop.classList.add('show');
    const modalContent = backdrop.querySelector('.modal');
    setTimeout(() => {
        modalContent.classList.add('show');
    }, 10);
    document.body.style.overflow = 'hidden';
}

/**
 * 关闭模态框
 */
function closeModal(backdrop) {
    const modal = backdrop.querySelector('.modal');
    modal.classList.remove('show');
    setTimeout(() => {
        backdrop.classList.remove('show');
        document.body.style.overflow = '';
    }, 300);
}

/**
 * 表格行悬停效果
 */
function initTableHover() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', function () {
                this.style.backgroundColor = 'rgba(0, 113, 227, 0.05)';
            });
            row.addEventListener('mouseleave', function () {
                this.style.backgroundColor = '';
            });
        });
    });
}

/**
 * 页面过渡动画
 */
function initPageTransitions() {
    // 获取所有内部链接
    const internalLinks = document.querySelectorAll('a[href^="/"], a[href^="./"], a[href^="../"], a[href^="' + window.location.origin + '"]');

    internalLinks.forEach(link => {
        // 排除带有target="_blank"的链接和下载链接
        if (link.getAttribute('target') !== '_blank' && !link.hasAttribute('download')) {
            link.addEventListener('click', function (e) {
                const href = this.getAttribute('href');

                // 排除锚点链接和JS链接
                if (href.startsWith('#') || href.startsWith('javascript:')) {
                    return;
                }

                e.preventDefault();
                showPageLoader();

                // 延迟跳转以展示加载动画
                setTimeout(() => {
                    window.location.href = href;
                }, 300);
            });
        }
    });

    // 页面加载完成后隐藏加载器
    window.addEventListener('load', hidePageLoader);
}

/**
 * 显示页面加载动画
 */
function showPageLoader() {
    const loader = document.querySelector('.loading-bar');
    if (loader) {
        loader.style.width = '70%';
        setTimeout(() => {
            loader.style.width = '90%';
        }, 200);
    }
}

/**
 * 隐藏页面加载动画
 */
function hidePageLoader() {
    const loader = document.querySelector('.loading-bar');
    if (loader) {
        loader.style.width = '100%';
        setTimeout(() => {
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.style.width = '0';
                loader.style.opacity = '1';
            }, 300);
        }, 500);
    }
}

/**
 * 表单验证初始化
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;

                    // 添加错误样式
                    field.classList.add('is-invalid');

                    // 如果不存在错误消息，则创建一个
                    let errorMsg = field.nextElementSibling;
                    if (!errorMsg || !errorMsg.classList.contains('invalid-feedback')) {
                        errorMsg = document.createElement('div');
                        errorMsg.className = 'invalid-feedback';
                        errorMsg.textContent = '此字段不能为空';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
            }
        });

        // 输入时移除错误样式
        form.querySelectorAll('input, select, textarea').forEach(field => {
            field.addEventListener('input', function () {
                this.classList.remove('is-invalid');
            });
        });
    });
}

/**
 * 重置筛选表单
 * @param {string} formId - 表单ID
 */
function resetFilters(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
        form.submit();
    }
}

/**
 * 获取选中的复选框值
 * @param {string} selector - 复选框选择器
 * @returns {Array} - 选中的值数组
 */
function getSelectedCheckboxValues(selector) {
    const checkboxes = document.querySelectorAll(selector + ':checked');
    return Array.from(checkboxes).map(checkbox => checkbox.value);
}

/**
 * 切换全选复选框
 * @param {string} selectAllId - 全选复选框ID
 * @param {string} checkboxSelector - 复选框选择器
 */
function toggleAllCheckboxes(selectAllId, checkboxSelector) {
    const selectAll = document.getElementById(selectAllId);
    const checkboxes = document.querySelectorAll(checkboxSelector);

    if (selectAll && checkboxes.length > 0) {
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAll.checked;
        });
    }
}

// 苹果风格平滑滚动
function smoothScroll(target, duration) {
    var targetElement = document.querySelector(target);
    if (!targetElement) return;

    var targetPosition = targetElement.getBoundingClientRect().top;
    var startPosition = window.pageYOffset;
    var distance = targetPosition - startPosition;
    var startTime = null;

    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        var timeElapsed = currentTime - startTime;
        var run = ease(timeElapsed, startPosition, distance, duration);
        window.scrollTo(0, run);
        if (timeElapsed < duration) requestAnimationFrame(animation);
    }

    function ease(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    }

    requestAnimationFrame(animation);
}

// 背景设置面板初始化
function initBackgroundSettings() {
    // 创建背景设置按钮
    createBackgroundSettingsToggle();

    // 创建背景设置面板
    createBackgroundSettingsPanel();

    // 加载保存的设置
    loadBackgroundSettings();
}

// 创建背景设置按钮
function createBackgroundSettingsToggle() {
    const body = document.body;
    const toggleBtn = document.createElement('div');
    toggleBtn.className = 'bg-settings-toggle';
    toggleBtn.innerHTML = '<i class="fas fa-cog"></i>';
    toggleBtn.title = '背景设置';

    toggleBtn.addEventListener('click', function () {
        const panel = document.querySelector('.bg-settings-panel');
        panel.classList.toggle('show');
    });

    body.appendChild(toggleBtn);
}

// 创建背景设置面板
function createBackgroundSettingsPanel() {
    const body = document.body;
    const panel = document.createElement('div');
    panel.className = 'bg-settings-panel';

    // 可选背景图片
    const bgImages = [
        { name: '默认', file: 'bg-default.jpg' },
        { name: '渐变蓝', file: 'bg-blue.jpg' },
        { name: '渐变紫', file: 'bg-purple.jpg' },
        { name: '渐变绿', file: 'bg-green.jpg' },
        { name: '细纹理', file: 'bg-texture.jpg' },
        { name: '抽象', file: 'bg-abstract.jpg' }
    ];

    let panelHTML = `
        <h4>背景设置</h4>
        <div class="form-group">
            <label>选择背景图片:</label>
            <div class="bg-preview">
    `;

    // 添加背景图片选项
    bgImages.forEach(bg => {
        panelHTML += `
            <div class="bg-option" 
                 style="background-image: url('/static/images/${bg.file}')" 
                 data-bg="${bg.file}" 
                 title="${bg.name}"></div>
        `;
    });

    panelHTML += `
            </div>
        </div>
        
        <div class="form-group opacity-control">
            <label>背景不透明度: <span id="opacity-value">70%</span></label>
            <input type="range" class="opacity-slider" id="bg-opacity" min="0" max="100" value="70">
        </div>
        
        <div class="form-group upload-bg">
            <label for="custom-bg">上传自定义背景:</label>
            <input type="file" id="custom-bg" class="form-control" accept="image/*">
        </div>
        
        <button class="btn btn-primary btn-sm" id="save-bg-settings">保存设置</button>
        <button class="btn btn-secondary btn-sm" id="reset-bg-settings">重置</button>
    `;

    panel.innerHTML = panelHTML;
    body.appendChild(panel);

    // 添加事件监听器
    setTimeout(() => {
        addBackgroundSettingsEvents();
    }, 100);
}

// 添加背景设置面板事件
function addBackgroundSettingsEvents() {
    // 背景图片选择
    const bgOptions = document.querySelectorAll('.bg-option');
    bgOptions.forEach(option => {
        option.addEventListener('click', function () {
            document.querySelectorAll('.bg-option.active').forEach(el => el.classList.remove('active'));
            this.classList.add('active');

            const bgFile = this.getAttribute('data-bg');
            document.body.style.backgroundImage = `url('/static/images/${bgFile}')`;
        });
    });

    // 背景不透明度调整
    const opacitySlider = document.getElementById('bg-opacity');
    const opacityValue = document.getElementById('opacity-value');

    opacitySlider.addEventListener('input', function () {
        const opacity = this.value / 100;
        opacityValue.textContent = `${this.value}%`;
        document.body.style.setProperty('--acrylic-opacity', opacity.toFixed(2));
        document.body.querySelector('body::before').style.backgroundColor = `rgba(255, 255, 255, ${1 - opacity})`;
    });

    // 自定义背景上传
    const customBgInput = document.getElementById('custom-bg');
    customBgInput.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                document.body.style.backgroundImage = `url('${e.target.result}')`;

                // 添加自定义背景选项
                const bgPreview = document.querySelector('.bg-preview');
                const customOption = document.createElement('div');
                customOption.className = 'bg-option active';
                customOption.style.backgroundImage = `url('${e.target.result}')`;
                customOption.setAttribute('data-bg', 'custom');
                customOption.title = '自定义背景';

                document.querySelectorAll('.bg-option.active').forEach(el => el.classList.remove('active'));
                bgPreview.appendChild(customOption);

                // 添加点击事件
                customOption.addEventListener('click', function () {
                    document.querySelectorAll('.bg-option.active').forEach(el => el.classList.remove('active'));
                    this.classList.add('active');
                    document.body.style.backgroundImage = `url('${e.target.result}')`;
                });
            };
            reader.readAsDataURL(file);
        }
    });

    // 保存设置
    const saveBtn = document.getElementById('save-bg-settings');
    saveBtn.addEventListener('click', function () {
        saveBackgroundSettings();

        // 关闭面板
        document.querySelector('.bg-settings-panel').classList.remove('show');

        // 显示提示
        showToast('设置已保存');
    });

    // 重置设置
    const resetBtn = document.getElementById('reset-bg-settings');
    resetBtn.addEventListener('click', function () {
        localStorage.removeItem('bgSettings');

        // 重置为默认背景
        document.body.style.backgroundImage = `url('/static/images/bg-default.jpg')`;
        document.body.style.setProperty('--acrylic-opacity', '0.85');
        document.querySelector('#bg-opacity').value = 70;
        document.querySelector('#opacity-value').textContent = '70%';

        // 重置选中状态
        document.querySelectorAll('.bg-option.active').forEach(el => el.classList.remove('active'));
        document.querySelector('.bg-option[data-bg="bg-default.jpg"]')?.classList.add('active');

        // 关闭面板
        document.querySelector('.bg-settings-panel').classList.remove('show');

        // 显示提示
        showToast('设置已重置');
    });
}

// 保存背景设置到本地存储
function saveBackgroundSettings() {
    const activeOption = document.querySelector('.bg-option.active');
    const opacityValue = document.getElementById('bg-opacity').value;

    let settings = {
        opacity: opacityValue,
        background: document.body.style.backgroundImage
    };

    if (activeOption) {
        settings.bgOption = activeOption.getAttribute('data-bg');
    }

    localStorage.setItem('bgSettings', JSON.stringify(settings));
}

// 加载背景设置
function loadBackgroundSettings() {
    const savedSettings = localStorage.getItem('bgSettings');

    if (savedSettings) {
        try {
            const settings = JSON.parse(savedSettings);

            // 设置背景图片
            if (settings.background) {
                document.body.style.backgroundImage = settings.background;
            }

            // 设置不透明度
            if (settings.opacity) {
                const opacity = settings.opacity / 100;
                document.getElementById('bg-opacity').value = settings.opacity;
                document.getElementById('opacity-value').textContent = `${settings.opacity}%`;
                document.body.style.setProperty('--acrylic-opacity', opacity.toFixed(2));
            }

            // 设置选中状态
            if (settings.bgOption) {
                setTimeout(() => {
                    const option = document.querySelector(`.bg-option[data-bg="${settings.bgOption}"]`);
                    if (option) {
                        document.querySelectorAll('.bg-option.active').forEach(el => el.classList.remove('active'));
                        option.classList.add('active');
                    }
                }, 200);
            }
        } catch (e) {
            console.error('加载背景设置出错', e);
        }
    }
}

// 显示提示框
function showToast(message, type = 'success') {
    // 检查是否已存在Toast
    let toast = document.querySelector('.toast-container');

    if (!toast) {
        toast = document.createElement('div');
        toast.className = 'toast-container';
        document.body.appendChild(toast);
    }

    const toastEl = document.createElement('div');
    toastEl.className = `toast toast-${type}`;
    toastEl.textContent = message;

    toast.appendChild(toastEl);

    // 动画显示
    setTimeout(() => {
        toastEl.classList.add('show');
    }, 10);

    // 3秒后自动移除
    setTimeout(() => {
        toastEl.classList.remove('show');
        setTimeout(() => {
            toastEl.remove();
        }, 300);
    }, 3000);
}

// 移动端导航
function initMobileNav() {
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarLinks = document.querySelector('.navbar-links');

    if (navbarToggle && navbarLinks) {
        navbarToggle.addEventListener('click', function () {
            navbarLinks.classList.toggle('show');
        });
    }
}

/**
 * 页面性能优化
 * 延迟加载非关键资源
 */
function optimizePageLoad() {
    // 延迟加载图片
    const lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // 回退方案，简单地加载所有图片
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
    }

    // 优化首页图表加载
    const chartContainers = document.querySelectorAll('.chart-container');
    if (chartContainers.length > 0) {
        // 延迟初始化图表，直到它们在视口中
        setTimeout(() => {
            initCharts();
        }, 100);
    }
}

/**
 * 拖放排序功能初始化
 */
function initSortable() {
    // 查找所有带有sortable类的容器
    const sortableContainers = document.querySelectorAll('.sortable');

    sortableContainers.forEach(container => {
        const items = container.querySelectorAll('.sortable-item');

        items.forEach(item => {
            // 设置可拖拽属性
            item.setAttribute('draggable', 'true');

            // 拖拽开始事件
            item.addEventListener('dragstart', function (e) {
                e.dataTransfer.setData('text/plain', this.dataset.id || this.id);
                this.classList.add('dragging');

                // 设置拖拽效果
                e.dataTransfer.effectAllowed = 'move';
            });

            // 拖拽结束事件
            item.addEventListener('dragend', function () {
                this.classList.remove('dragging');
            });
        });

        // 容器的拖拽事件处理
        container.addEventListener('dragover', function (e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';

            // 找到拖拽时的位置并处理元素顺序
            const dragging = container.querySelector('.dragging');
            if (!dragging) return;

            const siblings = [...container.querySelectorAll('.sortable-item:not(.dragging)')];
            const nextSibling = siblings.find(sibling => {
                const box = sibling.getBoundingClientRect();
                return e.clientY < box.top + box.height / 2;
            });

            if (nextSibling) {
                container.insertBefore(dragging, nextSibling);
            } else {
                container.appendChild(dragging);
            }
        });

        // 放置事件
        container.addEventListener('drop', function (e) {
            e.preventDefault();
            const id = e.dataTransfer.getData('text/plain');
            const draggedItem = document.getElementById(id) || container.querySelector(`[data-id="${id}"]`);

            // 获取新排序后的所有项目ID
            const newOrder = Array.from(container.querySelectorAll('.sortable-item'))
                .map(item => item.dataset.id || item.id);

            // 触发排序变更事件，可被外部代码捕获处理
            const sortEvent = new CustomEvent('sort-updated', {
                detail: {
                    container: container.id,
                    newOrder: newOrder
                }
            });
            document.dispatchEvent(sortEvent);

            // 如果有回调函数，则调用
            if (typeof onSortUpdate === 'function') {
                onSortUpdate(container.id, newOrder);
            }
        });
    });
}

// 此处仅为基本功能，详细功能将在后期实现 