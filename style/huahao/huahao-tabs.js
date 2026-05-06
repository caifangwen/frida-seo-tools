/**
 * Huahao Tab Component Switcher
 * 用于切换 hh-tabs 组件的 tab 面板
 * 使用方法：添加到 WordPress 代码片段插件（如 WPCode / Code Snippets）
 * 加载位置：Footer（页脚）
 */
(function() {
  'use strict';

  // 等待DOM加载完成
  document.addEventListener('DOMContentLoaded', function() {
    initHuahaoTabs();
  });

  // 如果DOM已经加载完成（延迟加载场景）
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    initHuahaoTabs();
  }

  function initHuahaoTabs() {
    // 查找所有带有 id 的 hh-tabs 容器
    var tabsContainers = document.querySelectorAll('.hh-tabs[id]');

    if (!tabsContainers.length) {
      return; // 没有tab组件，直接返回
    }

    tabsContainers.forEach(function(tabsContainer) {
      // 避免重复初始化
      if (tabsContainer.getAttribute('data-tab-initialized') === 'true') {
        return;
      }

      var tabButtons = tabsContainer.querySelectorAll('.hh-tab-btn');
      var tabPanels = tabsContainer.querySelectorAll('.hh-tab-panel');

      if (!tabButtons.length || !tabPanels.length) {
        return; // 按钮或面板缺失，跳过
      }

      // 初始化：隐藏所有非活动面板
      tabPanels.forEach(function(panel) {
        if (!panel.classList.contains('hh-active')) {
          panel.style.display = 'none';
        } else {
          panel.style.display = 'block';
        }
      });

      // 为每个tab按钮添加点击事件
      tabButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          e.preventDefault();

          var targetTab = this.getAttribute('data-tab');
          if (!targetTab) return;

          // 移除所有按钮的活动状态
          tabButtons.forEach(function(b) {
            b.classList.remove('hh-active');
            b.setAttribute('aria-selected', 'false');
          });

          // 隐藏所有面板
          tabPanels.forEach(function(p) {
            p.style.display = 'none';
            p.classList.remove('hh-active');
          });

          // 激活当前点击的按钮
          this.classList.add('hh-active');
          this.setAttribute('aria-selected', 'true');

          // 显示对应的面板
          var targetPanel = tabsContainer.querySelector('.hh-tab-panel[data-panel="' + targetTab + '"]');
          if (targetPanel) {
            targetPanel.style.display = 'block';
            targetPanel.classList.add('hh-active');
          }
        });

        // 添加键盘支持（Enter 和 Space）
        btn.addEventListener('keydown', function(e) {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            this.click();
          }
        });
      });

      // 标记为已初始化
      tabsContainer.setAttribute('data-tab-initialized', 'true');
    });
  }
})();
