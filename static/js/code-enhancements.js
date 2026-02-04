/**
 * Enhanced Code Block Features
 * - Copy button for code blocks
 * - Line number support
 */

document.addEventListener('DOMContentLoaded', function() {
    enhanceCodeBlocks();
});

function enhanceCodeBlocks() {
    const codeBlocks = document.querySelectorAll('pre');
    
    codeBlocks.forEach((block, index) => {
        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        wrapper.style.position = 'relative';
        wrapper.style.margin = '20px 0';
        
        // Add copy button
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-code-btn';
        copyBtn.innerHTML = '📋 Copy';
        copyBtn.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 6px 12px;
            background: rgba(201, 181, 156, 0.8);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85rem;
            z-index: 10;
            transition: all 0.2s;
        `;
        
        copyBtn.onmouseover = () => {
            copyBtn.style.background = '#C9B59C';
        };
        
        copyBtn.onmouseout = () => {
            copyBtn.style.background = 'rgba(201, 181, 156, 0.8)';
        };
        
        copyBtn.onclick = () => {
            const code = block.innerText;
            navigator.clipboard.writeText(code).then(() => {
                const originalText = copyBtn.innerHTML;
                copyBtn.innerHTML = '✅ Copied!';
                setTimeout(() => {
                    copyBtn.innerHTML = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        };
        
        // Insert wrapper and button
        block.parentNode.insertBefore(wrapper, block);
        wrapper.appendChild(block);
        wrapper.appendChild(copyBtn);
    });
}

/**
 * Smooth scroll for TOC links
 */
document.querySelectorAll('.toc-list a').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const href = link.getAttribute('href');
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
